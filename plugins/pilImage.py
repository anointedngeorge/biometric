from PIL import Image
import io
import os

# Assuming you have the file object in the 'photoFile' variable

def pil_image_file(request_uploaded_file, save_path:str, ext= 'JPEG'):
    '''
    *** request_uploaded_file: this is the file data from html form.
    *** save_path: this define directory path to save image
    *** ext: file extension to use. by default is in JPEG. This accepts only two format (jpg, jpeg)
    '''
    try:
        image_data = request_uploaded_file.read()
        # Create an in-memory stream
        image_stream = io.BytesIO(image_data)
        # Open the image using PIL
        image = Image.open(image_stream)
        # Check if the image format is JPEG
        if image.format != 'JPEG':
            # Convert the image to JPEG format
            image = image.convert('RGB')
        # Save the image with .jpeg extension
        image.save(save_path, ext)
        # Close the image
        image.close()
    except Exception as e:
        print(e)



def load_image_dir(base_dir:str):
    '''
    base_dir: this define the path where image directory is located.

    '''
    try:
        files = {}
        directory =  os.listdir(base_dir)
        extensions = ('.jpg','.jpeg')
        if directory:
            for file in directory:
                if file.endswith(extensions):
                    path_dir =  os.path.join(base_dir, file)
                    filename =  file.split('.')[0]
                    files[filename] = path_dir
        return files
    except Exception as e:
        print(e)
