import cv2
import os
import numpy as np

# Directory containing the photos
photo_directory = 'frontend/media/photo/'

# List all files in the photo directory
photo_files = os.listdir(photo_directory)

# Prepare the dataset and labels
dataset = []     # List to store preprocessed face images
labels = []      # List to store corresponding labels

# Load the pre-trained face classifier
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Loop through each file in the photo directory
for photo_file in photo_files:
    photo_dirs = os.path.join(photo_directory, photo_file)
    if os.path.isdir(photo_dirs):
        photo_dir_path =  photo_dirs
        for photo_to_file in os.listdir(photo_dirs):
            photo_path =  f"{photo_dir_path}/{photo_to_file}"
#             # Read the photo
            photo = cv2.imread(photo_path)
            gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
            # Detect faces in the photo
            faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    # Process each detected face
    for (x, y, w, h) in faces:
        # Extract the face region
        face = gray[y:y+h, x:x+w]

        # Resize the face to a fixed size for training
        face = cv2.resize(face, (100, 100))

        # Add the face image and label to the dataset
        dataset.append(face)
        labels.append(photo_file)  # Use the photo file name as the label

# Convert dataset to numpy array
dataset = np.array(dataset)

# Create label encoding dictionary
label_encoding = {label: index for index, label in enumerate(set(labels))}

# Convert labels to integer values
labels_encoded = [label_encoding[label] for label in labels]

# Convert labels to cv2.UMat
labels_umat = cv2.UMat(np.array(labels_encoded))

# Create an LBPH recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Train the recognizer with the dataset and labels
recognizer.train(dataset, labels_umat)

# Save the trained model to a file
model_path = 'trained_models/model.yml'
recognizer.save(model_path)
