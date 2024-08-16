from datetime import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Image

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
            # Generate a unique filename to avoid conflicts
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file_obj.name}"

            # Save the file to MinIO using django-storages
            file_path = default_storage.save(filename, ContentFile(file_obj.read()))

            # Create Image model instance
            image_instance = Image.objects.create(image=file_path)

            return Response({
                'message': 'Image stored successfully',
                'image_url': image_instance.minio_url
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'Failed to upload image: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)