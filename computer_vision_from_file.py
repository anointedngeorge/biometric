import face_recognition
import cv2
import csv
import glob
from datetime import datetime
import os
import numpy as np
import time
photo_path_directory =  'frontend/media/photo'

test_photo_path_directory =  'frontend/media/test_photo/biden3.jpg'

def load_single_file(file = 'andrew.jpeg'):
    known_face_encodings = []
    known_face_names = ''
    file_extentions = ('.jpeg','jpg','.png')

    for photo_file in os.listdir(photo_path_directory):
        # print(photo_file)
        if not os.path.isdir(os.path.join(photo_path_directory, photo_file)):
            photo_dir = os.path.join(photo_path_directory, photo_file)
            # filename
            filename = photo_file.split('.')[0]
            # check if file extension is permitted
            if photo_dir.lower().endswith(file_extentions):
                image = face_recognition.load_image_file(photo_dir)
                image_encoding = face_recognition.face_encodings(image)[0]
                known_face_encodings.append(image_encoding)
                # known_face_names.append(filename)
                known_face_names =  filename
    return known_face_encodings, known_face_names
  
def window():
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    file_encoding, known_face_names= load_single_file()  # Load the face encoding from a single file

    while True:
        # Grab a single frame from the loaded file
        frame = cv2.imread(test_photo_path_directory)

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(file_encoding, face_encoding)
                name = "Unknown"
                if True in matches:
                    # name = "Loaded File"
                    name = known_face_names + " Present"
                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        # Display the resulting image
        cv2.imshow("Biometric Student Attendance", frame)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

window()