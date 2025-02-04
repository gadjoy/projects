import os
import googlemaps
from datetime import datetime, timedelta
from dotenv import load_dotenv
from django.http import JsonResponse, HttpResponse
from django.urls import path
from django.core.management import execute_from_command_line
from django.conf import settings
import corsheaders  # Ensure you import corsheaders

# Load environment variables from .env file
load_dotenv()

# Retrieve the secret key and Google Maps API key from environment variables
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Initialize Google Maps Client
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# Ensure SECRET_KEY is set
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables")

# Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")
settings.configure(
    DEBUG=True,
    SECRET_KEY=SECRET_KEY,
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    MIDDLEWARE=[
        'corsheaders.middleware.CorsMiddleware',  # CORS middleware is placed here
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ],
    INSTALLED_APPS=[
        'corsheaders',  # Make sure 'corsheaders' is included in INSTALLED_APPS
        "django.contrib.contenttypes",
    ],
    CORS_ALLOWED_ORIGINS=[  # Allow your frontend's origin
        "http://localhost:5174",  # Ensure this matches your frontend URL
    ],
)

class TrafficAnalyzer:
    def __init__(self, api_key):
        self.gmaps = googlemaps.Client(key=api_key)

    def get_route_with_traffic(self, source, destination, departure_time):
        directions = self.gmaps.directions(
            source,
            destination,
            mode="driving",
            departure_time=departure_time,
            traffic_model="best_guess"
        )
        if directions and len(directions) > 0:
            leg = directions[0]['legs'][0]
            return {
                "duration_in_traffic": leg['duration_in_traffic']['text'],
                "duration_in_traffic_minutes": leg['duration_in_traffic']['value'] // 60,
                "distance": leg['distance']['text']
            }
        else:
            raise ValueError("No route found")

    def get_traffic_level(self, travel_time_minutes):
        if travel_time_minutes <= 30:
            return "Low"
        elif 30 < travel_time_minutes <= 60:
            return "Medium"
        else:
            return "High"

    def generate_traffic_slots(self, source, destination):
        now = datetime.now()
        if now.minute > 0:  # Adjust to the next half hour
            now = now.replace(second=0, microsecond=0) + timedelta(minutes=(30 - now.minute % 30))

        slots = []

        for half_hour_offset in range(48):  # 48 slots for 24 hours (30-minute intervals)
            slot_start_time = now + timedelta(minutes=half_hour_offset * 30)
            if 0 <= slot_start_time.hour < 6:  # Exclude slots from 12:00 AM to 6:00 AM
                continue

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

        # Sort slots by travel time
        sorted_slots = sorted(slots, key=lambda x: x['travel_time_in_minutes'])

        # Get top 3 shortest and longest slots
        shortest_slots = sorted_slots[:3]
        longest_slots = sorted_slots[-3:]

        return {
            "source": source,
            "destination": destination,
            "total_distance": shortest_slots[0]['distance'] if shortest_slots else "N/A",
            "shortest_slots": shortest_slots,
            "longest_slots": longest_slots
        }

    def calculate_saved_time(self, slot1, slot2):
        saved_time = (slot1['travel_time_in_minutes'] + slot2['travel_time_in_minutes']) - 120
        return saved_time

# Views
def home(request):
    return HttpResponse("Welcome to the Quick Reach backend! Use /traffic_slots/ for traffic analysis.")

def traffic_slots(request):
    source = request.GET.get("source")
    destination = request.GET.get("destination")

    if not source or not destination:
        return JsonResponse({"error": "Both 'source' and 'destination' must be provided"}, status=400)

    analyzer = TrafficAnalyzer(GOOGLE_MAPS_API_KEY)
    result = analyzer.generate_traffic_slots(source, destination)

    return JsonResponse(result)

def test_backend(request):
    return JsonResponse({"message": "Backend is running successfully!"})

# URL patterns
urlpatterns = [
    path('', home),  # Route for the root URL
    path('traffic_slots/', traffic_slots),
    path('test/', test_backend),
]

# Run the Django application
if __name__ == "__main__":
    execute_from_command_line(['manage.py', 'runserver'])
