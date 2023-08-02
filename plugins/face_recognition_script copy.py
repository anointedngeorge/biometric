import face_recognition
import cv2
import csv
import glob
from datetime import datetime
import numpy as np
import time
import os
from authuser.models import StudentModel

VIDEO_TITLE =  'Biometric Student Attendance'



def load_photo_file(photo_path_directory='frontend/media/photo'):
    known_face_encodings = []
    known_face_names = []
    file_extentions = ('.jpeg','.jpg','.png')
    
    for photo_file in os.listdir(photo_path_directory):
        # print(photo_file)
        if not os.path.isdir(os.path.join(photo_path_directory, photo_file)):
            photo_dir = os.path.join(photo_path_directory, photo_file)
            # filename
            filename = photo_file.split('.')[0]
            # check if file extension is permitted
            if photo_dir.lower().endswith(file_extentions):
                image = face_recognition.load_image_file(photo_dir)
                image_encoding = face_recognition.face_encodings(image)
                if len(image_encoding) > 0:
                    known_face_encodings.append(image_encoding[0])
                    known_face_names.append(filename)
    # return result
    return known_face_encodings, known_face_names

    
# known_face_encodings , known_face_names = load_photo_file()

def VideoCaptureFrame(known_face_encodings , known_face_names, title, username='', delay =50):
    face_locations = []
    face_encodings = []
    face_names = []
    choosen_name = ''
    process_this_frame = True
    match_found = False
    counter = 0
    # student_id = None


    video_capture = cv2.VideoCapture(0)

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
                # # If a match was found in known_face_encodings, just use the first one.
            
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
    
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    student = StudentModel.objects.all()
                    if student.filter(picture_name= name).exists():
                        student =  student.filter(picture_name= name).get()
                        frame_title = f"{student.first_name} {student.last_name} delay: {delay}-({delay-counter}) "
                        student_id =  student.id
                    # this will allow for a delay before breaking the loop
                    if counter > delay:
                        match_found = True  # Set the flag to True if a match is found
                        choosen_name += str(student_id)
                        break  # Exit the loop
                    counter = counter + 1
                    # time.sleep(5)
                face_names.append(frame_title)

                if True in matches:
                    first_match_index = matches.index(True)
                    # name = known_face_names[first_match_index] if username == '' else username
        # process_this_frame = not process_this_frame
        
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
        return 	match_found, choosen_name

