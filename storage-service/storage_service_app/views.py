from datetime import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Image
import requests
import os

class ImageUploadAPI(APIView):
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        """
        Store Image API Endpoint

        This endpoint allows users to upload an image file and store it in both the database and MinIO S3-compatible storage.

        Method: POST
        Endpoint: /api/store/
        Content-Type: multipart/form-data

        Request:
        - file: The image file to be uploaded (required)

        Response:
        - 201 Created: Image uploaded successfully
          {
            "message": "Image stored successfully",
            "image_url": "http://minio:9000/images/filename.jpg"
          }
        - 400 Bad Request: No file in request or upload failed
          {
            "error": "Error message"
          }

        Example usage with curl:
        curl -X POST http://localhost:8000/api/store/ \
          -H 'Content-Type: multipart/form-data' \
          -F 'file=@/path/to/your/image.jpg'

        Notes:
        - Ensure the MinIO server is running and accessible.
        - The image will be stored in the MinIO 'images' bucket.
        - The Image model will store metadata about the uploaded image, including its MinIO URL.
        """

        file_obj = request.FILES.get('file')
    
        if not file_obj:
            return Response({'error': 'No file found in request'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            file_content = file_obj.read()
            
            file_contents = ContentFile(file_content)
            file_contents_aux = file_contents

            try:
                file_contents_baw = requests.post(
                    "http://black-white:80/upload",
                    files={'image': file_contents_aux}
                )

                img_baw = ContentFile(file_contents_baw.content)

                print(img_baw)
                print(file_contents)
            except Exception as e:
                print(e)

            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file_obj.name}"

            file_path = default_storage.save(filename, img_baw)

            image_instance = Image.objects.create(image=file_path)

            needed_information = requests.post(
                "http://textDetection:80/api/process-image/",
                files={'image_with_password': ContentFile(file_content, name=filename)}
            )

            weHaveAutio = False
            try:
                audioFile = requests.post(
                    "http://ttsapp:80/api/listen/",
                    data={"text": str(needed_information.json())},
                    timeout=10  
                )
                audioFile.raise_for_status() 
                weHaveAutio = True 
            except Exception as e:
                print(e)

            data = {
                "sender": "andreidabreanu123@gmail.com",
                "receiver": "pdobrescu@luminess.eu",
                "text": f"Credentialele tale în JSON sunt {needed_information.json()}",
                "password": "axvjsluwogohmfma"
            }

            files = None
            if weHaveAutio:
                files = {"audio": ("audio.mp3", audioFile.content, "audio/mpeg")}

            try:
                trimiteInformatiiPeMail = requests.post(
                    "http://emailsender:80/api/send-mail/",
                    data=data,
                    files=files  
                )

                if trimiteInformatiiPeMail.status_code == 200:
                    print("Email sent successfully!")
                else:
                    print(f"Failed to send email. Status code: {trimiteInformatiiPeMail.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
            
            return Response({
                'message': 'Image stored successfully',
                'image_url': image_instance.minio_url
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'Failed to upload image: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)