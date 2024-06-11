import webbrowser
import os

# Define the path to the HTML file
html_file = 'camera.html'

# Get the absolute path to the HTML file
abs_path = os.path.abspath(html_file)
print(f"Opening file: {abs_path}")

# Open the HTML file in the default web browser
webbrowser.open('file://' + abs_path)
