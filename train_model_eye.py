import cv2
import os
import numpy as np

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    dataset = []
    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (100, 100))
        dataset.append(face)
    return dataset

def encode_labels(labels):
    unique_labels = set(labels)
    label_encoding = {label: index for index, label in enumerate(unique_labels)}
    labels_encoded = [label_encoding[label] for label in labels]
    return labels_encoded

def train_eye_recognition_model(photo_directory, model_path):
    photo_files = os.listdir(photo_directory)
    dataset = []
    labels = []
    for photo_file in photo_files:
        photo_path = os.path.join(photo_directory, photo_file)
        if os.path.isdir(photo_path):
            for file in os.listdir(photo_path):
                image_path = os.path.join(photo_path, file)
                image = cv2.imread(image_path)
                preprocessed_images = preprocess_image(image)
                dataset.extend(preprocessed_images)
                labels.extend([photo_file] * len(preprocessed_images))
    dataset = np.array(dataset)
    labels_encoded = encode_labels(labels)
    labels_umat = cv2.UMat(np.array(labels_encoded))
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(dataset, labels_umat)
    recognizer.save(model_path)

# Directory containing the photos
photo_directory = 'frontend/media/photo/'

# Save the trained model to a file
model_path = 'trained_models/model.yml'

# Train the eye recognition model
train_eye_recognition_model(photo_directory, model_path)
