from flask import Flask, render_template, request, redirect, url_for
import random
import string

app = Flask(__name__)

# Custom Base URL (change this to your deployed domain)
BASE_URL = "http://127.0.0.1:5000/"  # For local testing, change this when deploying

# Dictionary to store the shortened URLs
url_mapping = {}

# Function to generate a random short URL code
def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    
    # Check if the URL is already shortened
    if original_url in url_mapping:
        short_code = url_mapping[original_url]
    else:
        short_code = generate_short_code()
        url_mapping[original_url] = short_code

    # Return the short URL with the custom BASE_URL and the short code
    short_url = BASE_URL + short_code
    return render_template('index.html', short_url=short_url, short_code=short_code)

@app.route('/<short_code>')
def redirect_to_url(short_code):
    # Find the original URL by matching the short code
    for original_url, code in url_mapping.items():
        if code == short_code:
            return redirect(original_url)

    # If short code not found, show a 404 error
    return "<h1>URL not found</h1>", 404

if __name__ == '__main__':
    app.run(debug=True)
