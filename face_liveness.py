import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow INFO logs
import tensorflow as tf
import cv2
import numpy as np
from tensorflow.keras.models import load_model

class FaceLiveness:
    def __init__(self, model_path):
        # Load pre-trained liveness detection model
        self.model = load_model(model_path)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def preprocess_face(self, face):
        # Resize and normalize the face to match model input
        resized_face = cv2.resize(face, (150, 150))   # Model expects 150x150
        normalized_face = resized_face / 255.0        # Normalize pixel values
        return np.expand_dims(normalized_face, axis=0)  # Add batch dimension (1, 150, 150, 3)

    def detect_liveness(self, frame):
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) > 1:
            return "multiple_faces", len(faces)

        for (x, y, w, h) in faces:
            # Crop and preprocess the face
            face = frame[y:y+h, x:x+w]
            preprocessed_face = self.preprocess_face(face)

            # Predict liveness
            prediction = self.model.predict(preprocessed_face, verbose=0)[0][0]
            if prediction > 0.5:  # Threshold for real vs spoof
                return "real", len(faces)
            else:
                return "spoof", len(faces)

        return "no_face", len(faces)  # If no face detected
