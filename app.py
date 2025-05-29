from flask import Flask, request, jsonify, render_template, redirect, url_for
from face_liveness import FaceLiveness
import cv2
import numpy as np
import base64
import logging

app = Flask(__name__, static_url_path='/static')
detector = FaceLiveness(model_path="liveness_model.h5")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Main page with both options

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Replace with actual authentication logic
    if username == "admin" and password == "password":
        return redirect(url_for("face_detection"))
    else:
        return render_template("index.html", error="Invalid username or password")

@app.route("/face-detection")
def face_detection():
    return render_template("face_detection.html")

@app.route("/verify_liveness", methods=["POST"])
def verify_liveness():
    try:
        data = request.json.get("image")
        if not data:
            return jsonify({"success": False, "message": "No image provided"})

        image_data = base64.b64decode(data.split(",")[1])
        np_img = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        result, face_count = detector.detect_liveness(frame)

        if face_count > 1:
            return jsonify({"success": False, "message": "Multiple faces detected! Please ensure only one person is in the frame."})

        if result == "real":
            return jsonify({"success": True, "message": "Liveness confirmed!"})
        elif result == "spoof":
            return jsonify({"success": False, "message": "Spoof detected!"})
        else:
            return jsonify({"success": False, "message": "No face detected!"})

    except Exception as e:
        logger.error(f"Error during liveness detection: {e}")
        return jsonify({"success": False, "message": "An error occurred during processing."})

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

if __name__ == "__main__":
    app.run(debug=True)
