from django.core.files.storage import get_storage_class
from django.conf import settings





def read_from_s3(file_path):
    import face_recognition
    known_face_encodings = []
    known_face_names = []
    # Get the S3BotoStorage class instance
    s3_storage = get_storage_class(settings.DEFAULT_FILE_STORAGE)()

    # Provide the file path to the file you want to read
    # 'file_path' should be the relative path of the file in your S3 bucket
    try:
        with s3_storage.open(file_path, 'rb') as file:
            image = face_recognition.load_image_file(file)
            image_encoding = face_recognition.face_encodings(image)

            if len(image_encoding) > 0:
                known_face_encodings.append(image_encoding[0])
                remove_photo_from_path =  str(file).replace('photo/','')
                known_face_names.append(remove_photo_from_path.split('.')[0])
            #  known_face_encodings, known_face_names
            return known_face_encodings, known_face_names
        
    except FileNotFoundError:
        # Handle the case when the file is not found
        print("File not found.")
        return None
    except Exception as e:
        return f"Error occurred: {e}"

# Example usage:
# file_path = 'path/to/your/file.txt'
# file_content = read_from_s3(file_path)
# if file_content:
#     print(file_content)





def get_relative_path(absolute_url, base_url):
    # Remove the base URL from the absolute URL
    relative_path = absolute_url.replace(base_url, "", 1)
    # Remove any query parameters, if present
    relative_path = relative_path.split("?")[0]
    # Remove any leading or trailing slashes (optional, depending on your preference)
    relative_path = relative_path.strip("/")
    return relative_path