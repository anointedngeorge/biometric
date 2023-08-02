import cv2
import base64
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        await self.accept()

    
        try:
            video_capture = cv2.VideoCapture(0)
            
            if not video_capture.isOpened():
                raise Exception("Could not open video capture.")
            
            
            while True:
            
                ret, frame = video_capture.read()
                print(frame)
                # if not ret:
                #     break

                # Process the frame here (e.g., face detection, etc.)
                # For simplicity, we're not doing any processing here.
                # You can add your image processing code as needed.

                # Encode the frame to JPEG format
                # _, jpeg_frame = cv2.imencode('.jpg', frame)
               
                # # Base64 encode the bytes and convert to a string
                # encoded_frame = base64.b64encode(jpeg_frame.tobytes()).decode('utf-8')
                
                # # print(encoded_frame)
                # # Send the frame as a string to the client
                # await self.send(encoded_frame)

        finally:
            # video_capture.release()
            pass
