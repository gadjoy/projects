import os
import googlemaps
from datetime import datetime, timedelta
from dotenv import load_dotenv
from django.http import JsonResponse, HttpResponse
from django.urls import path
from django.core.management import execute_from_command_line
from django.conf import settings
from googlemaps.exceptions import ApiError

# Load environment variables
load_dotenv()

# Retrieve API keys
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-default-secret-key")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "your-google-maps-api-key")

if not GOOGLE_MAPS_API_KEY:
    raise ValueError("GOOGLE_MAPS_API_KEY must be set in the environment variables")

# Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")
settings.configure(
    DEBUG=True,
    SECRET_KEY=SECRET_KEY,
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    MIDDLEWARE=[
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
    ],
    INSTALLED_APPS=[
        'corsheaders',
        "django.contrib.contenttypes",
    ],
    CORS_ALLOWED_ORIGINS=[
        "http://localhost:5173",
    ],
    CORS_ALLOW_CREDENTIALS=True,
)

class TrafficAnalyzer:
    def __init__(self, api_key):
        self.gmaps = googlemaps.Client(key=api_key)

    def get_route_with_traffic(self, source, destination, departure_time):
        try:
            directions = self.gmaps.directions(
                source,
                destination,
                mode="driving",
                departure_time=departure_time,
                traffic_model="best_guess"
            )
            if directions and directions[0]['legs']:
                leg = directions[0]['legs'][0]
                return {
                    "duration_in_traffic": leg['duration_in_traffic']['text'],
                    "duration_in_traffic_minutes": leg['duration_in_traffic']['value'] // 60,
                    "distance": leg['distance']['text']
                }
            else:
                raise ValueError("No route found")
        except ApiError as e:
            raise ValueError(f"Google Maps API Error: {e}")

    def get_traffic_level(self, travel_time_minutes):
        if travel_time_minutes <= 30:
            return "Low"
        elif 30 < travel_time_minutes <= 60:
            return "Medium"
        else:
            return "High"

    def generate_traffic_slots(self, source, destination):
        now = datetime.now().replace(second=0, microsecond=0)
        if now.minute > 0:
            now += timedelta(minutes=(30 - now.minute % 30))

        slots = []
        for half_hour_offset in range(48):
            slot_start_time = now + timedelta(minutes=half_hour_offset * 30)

            if 0 <= slot_start_time.hour < 6:
                continue  # Skip 12 AM - 6 AM slots

            try:
                route_details = self.get_route_with_traffic(
                    source,
                    destination,
                    departure_time=int(slot_start_time.timestamp())
                )
                slots.append({
                    "slot_time_range": f"{slot_start_time.strftime('%I:%M %p')} - "
                                       f"{(slot_start_time + timedelta(minutes=30)).strftime('%I:%M %p')}",
                    "estimated_travel_time": route_details['duration_in_traffic'],
                    "travel_time_in_minutes": route_details['duration_in_traffic_minutes'],
                    "distance": route_details['distance'],
                    "traffic_level": self.get_traffic_level(route_details['duration_in_traffic_minutes'])
                })
            except ValueError as e:
                print(f"Skipping slot at {slot_start_time}: {e}")
                continue

        return {
            "source": source,
            "destination": destination,
            "total_distance": slots[0]['distance'] if slots else "N/A",
            "traffic_slots": slots
        }

# Views
def home(request):
    return HttpResponse("Welcome to Quick Reach API! Use /traffic_slots/")

def traffic_slots(request):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET requests are allowed"}, status=405)

    source = request.GET.get("source")
    destination = request.GET.get("destination")

    if not source or not destination:
        return JsonResponse({"error": "Both 'source' and 'destination' must be provided"}, status=400)

    analyzer = TrafficAnalyzer(GOOGLE_MAPS_API_KEY)
    try:
        result = analyzer.generate_traffic_slots(source, destination)
        return JsonResponse(result)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=500)

# URL patterns
urlpatterns = [
    path('', home),
    path('traffic_slots/', traffic_slots),
]

# Run server
if __name__ == "__main__":
    execute_from_command_line(['manage.py', 'runserver'])
