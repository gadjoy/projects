from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import atexit
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Allow CORS for the specific origin where your Vue app is running (http://localhost:8080)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

# Access API key from environment variable
api_key = os.getenv('API_KEY')

# Initialize APScheduler
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# In-memory store for scheduled posts
scheduled_posts = []

# Helper function to post content to social media (for demonstration purposes)
def post_to_social_media(content):
    print(f"Posting to social media: {content}")

# Home Route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to AutoReach API!"})

# Content Generation Route
@app.route('/generate_content', methods=['POST'])
def generate_content():
    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    detailed_prompt = (
        f"Generate engaging and creative social media content for both Instagram and Twitter based on the following information: {prompt}. "
        f"Ensure that the generated content is well-structured with headings in bold and content presented in bullet points. "
        f"Include a detailed ad campaign plan in the response."
    )

    request_body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": detailed_prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}",
        json=request_body,
    )

    # Debugging output
    print("AI API Response Code:", response.status_code)
    print("AI API Response Text:", response.text)

    if response.status_code != 200:
        return jsonify({"error": response.json()}), response.status_code

    response_data = response.json()
    generated_text = response_data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

    if not generated_text:
        return jsonify({"error": "No content generated"}), 500

    # Format the generated text (HTML-like structure for headings and bullet points)
    formatted_content = generated_text.replace('**', '<b>').replace('\n- ', '<li>').replace('\n\n', '</li></ul><br><b>')
    formatted_content = f"<b>{formatted_content}</b><ul>"

    # Split Instagram, Twitter, and Ad Campaign sections
    sections = formatted_content.split('<br><b>Ad Campaign Details</b><br>')
    instagram_twitter_content = sections[0].strip() if len(sections) > 0 else "No Instagram and Twitter content generated."
    ad_campaign_content = sections[1].strip() if len(sections) > 1 else "No ad campaign generated."

    response_result = {
        'instagram_twitter_content': instagram_twitter_content,
        'ad_campaign_content': ad_campaign_content
    }

    return jsonify(response_result)

# Scheduling Post Route
@app.route('/schedule_post', methods=['POST'])
def schedule_post():
    data = request.json
    content = data.get("content")
    scheduled_time = data.get("scheduled_time")

    if not content or not scheduled_time:
        return jsonify({"error": "Missing content or scheduled time"}), 400

    # Convert the scheduled_time to a datetime object
    try:
        schedule_time = datetime.strptime(scheduled_time, "%Y-%m-%dT%H:%M")
    except ValueError:
        return jsonify({"error": "Invalid scheduled time format. Use YYYY-MM-DDTHH:MM."}), 400

    # Schedule the post using APScheduler
    scheduler.add_job(func=post_to_social_media, trigger='date', run_date=schedule_time, args=[content])

    # Store the scheduled post in memory (or save in a database)
    scheduled_posts.append({"content": content, "scheduled_time": schedule_time})

    return jsonify({"message": "Post scheduled successfully!"})

# Retrieve scheduled posts
@app.route('/get_scheduled_posts', methods=['GET'])
def get_scheduled_posts():
    formatted_posts = [{"content": post["content"], "scheduled_time": post["scheduled_time"].strftime("%Y-%m-%d %H:%M")} for post in scheduled_posts]
    return jsonify(formatted_posts)

# Ad Campaign Automation Route
@app.route('/ad_campaign_automation', methods=['POST'])
def ad_campaign_automation():
    data = request.json
    ad_content = data.get("ad_content")
    performance_metrics = data.get("performance_metrics")
    budget = data.get("budget")

    if not ad_content or not performance_metrics:
        return jsonify({"error": "Ad content or performance metrics missing"}), 400

    # Here, you would integrate with the Google AdWords API and apply optimizations.
    optimized_ad = {
        "optimizedAdCopy": f"Optimized Ad: content about {ad_content} in 50 words to post on Instagram and Twitter - Now with enhanced engagement!",
        "suggestedBid": 10.0,  # Example bid
        "budgetAdjustment": budget + 50,  # Example budget adjustment
        "performanceMetrics": performance_metrics  # Return the same performance metrics for now
    }

    return jsonify(optimized_ad)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
