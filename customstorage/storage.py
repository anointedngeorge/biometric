from django.core.exceptions import SuspiciousFileOperation
from django.core.files.storage import FileSystemStorage
from django.utils._os import safe_join

class CustomStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None):
        super().__init__(location, base_url)

    def _save(self, name, content):
        file_content =  content.read()
        # Check if the name contains a path traversal attempt
        if "../" in name:
            raise SuspiciousFileOperation("Detected path traversal attempt.")

        # Use safe_join to ensure the path is safe and normalized
        path = safe_join(self.location, name)
        print(path)
        # Open the file in write-binary mode
        with self.open(path, 'wb') as destination:
            # Iterate over the chunks of the uploaded file
            for chunk in content.chunks():
                destination.write(chunk)

        # Return the path where the file is saved
        return name
