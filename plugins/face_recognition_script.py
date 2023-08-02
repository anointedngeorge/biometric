import face_recognition
import cv2
import csv
from datetime import datetime
import numpy as np
import time
import os
from django.core.files.storage import default_storage
from storages.backends.s3boto3 import S3Boto3Storage
from authuser.models import StudentModel
from decouple import config

VIDEO_TITLE = 'Biometric Student Attendance'


def load_photo_file_storage():
    from plugins.boto_plugins import read_from_s3, get_relative_path
    base_url = "https://bucketeer-67381f08-9445-4469-87fb-4ea24093de1e.s3.amazonaws.com/"

    container1 = []
    container2 = []

    try:
        from django.core.files.storage import default_storage
        from authuser.models import StudentModel
        students =  StudentModel.objects.all()

        if students.exists:
            for student in students:
                relative_path = get_relative_path(student.picture_url.url, base_url)
                # file_path = 'path/to/your/file.txt'
                known_face_encodings, known_face_names = read_from_s3(relative_path)

                if known_face_encodings:
                    container1.extend(known_face_encodings)
                    container2.extend(known_face_names)
                    
    except Exception as e :
        return ("Database: %s " %e)
    
    return container1, container2



def load_photo_file(photo_path_directory='photo'):
    known_face_encodings = []
    known_face_names = []
    file_extentions = ('.jpeg', '.jpg', '.png')
    photo_files = None
   
    photo_files = default_storage.listdir(photo_path_directory)[1]

    for photo_file in photo_files:
        # Check if file extension is permitted
        if photo_file.lower().endswith(file_extentions):
            # Read the image file from media storage
            with default_storage.open(os.path.join(photo_path_directory, photo_file), 'rb') as file:
                image = face_recognition.load_image_file(file)
                image_encoding = face_recognition.face_encodings(image)
                if len(image_encoding) > 0:
                    known_face_encodings.append(image_encoding[0])
                    known_face_names.append(photo_file.split('.')[0])

    # Return result
    return known_face_encodings, known_face_names


# known_face_encodings, known_face_names = load_photo_file()

def video1():
    try:
        video_capture = cv2.VideoCapture(0)

        # Check if the video capture was successful
        if not video_capture.isOpened():
            raise Exception("Could not open video capture.")

        while True:
            ret, frame = video_capture.read()

            # Display the resulting image
            cv2.imshow('title', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

    except Exception as e:
        return str(e)


def VideoCaptureFrame(known_face_encodings, known_face_names, title, username='', delay=50):
    try:
        face_locations = []
        face_encodings = []
        face_names = []
        choosen_name = ''
        process_this_frame = True
        match_found = False
        counter = 0

        video_capture = cv2.VideoCapture(0)
        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        while not match_found:
            # Grab a single frame of video
            ret, frame = video_capture.read()
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
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    frame_title = "Unknown Student"

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        student = StudentModel.objects.filter(picture_name=name).first()
                        # print(StudentModel.objects.filter(picture_name=name),  'student')
                        if student:
                            frame_title = f"{student.first_name} {student.last_name} delay: {delay}-({delay - counter}) "
                            student_id = student.id
                            if counter > delay:
                                match_found = True  # Set the flag to True if a match is found
                                choosen_name += str(student_id)
                                break  # Exit the loop
                            counter = counter + 1

                    face_names.append(frame_title)

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
                cv2.putText(frame, frame_title, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow(title, frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

        if match_found:
            # Perform actions or return data
            # Example: Return the matched name
            return match_found, choosen_name
    except Exception as e:
        return f'{e}'