from flask import Flask, render_template, request, redirect
import dlib
import cv2
import numpy as np
import base64

app = Flask(__name__)

# Load the pre-trained facial landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Route for rendering the index.html template
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if file:
            # Read the image file
            image_stream = file.read()
            nparr = np.frombuffer(image_stream, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Convert image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Convert the original image to base64 for displaying
            _, img_encoded = cv2.imencode('.jpg', image)
            img_base64 = base64.b64encode(img_encoded).decode('utf-8')

            # Detect faces in the image
            faces = detector(gray)

            # Draw landmarks and face detection box on the image
            for face in faces:
                landmarks = predictor(gray, face)
                for n in range(0, 68):
                    x = landmarks.part(n).x
                    y = landmarks.part(n).y
                    cv2.circle(image, (x, y), 1, (0, 0, 255), 2)  # Red color for landmarks
                # Draw a rectangle around the face
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green color for face box

            # Convert the image with landmarks to base64 for displaying
            _, img_landmarks_encoded = cv2.imencode('.jpg', image)
            img_landmarks_base64 = base64.b64encode(img_landmarks_encoded).decode('utf-8')

            return render_template("index.html", img_base64=img_base64, img_landmarks_base64=img_landmarks_base64)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
