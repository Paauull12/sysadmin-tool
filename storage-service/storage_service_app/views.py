from datetime import datetime
from pathlib import Path

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from storage_service import settings
from .models import Image


class ImageUploadAPI(APIView):
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        """
        Store Image API Endpoint Documentation

        This API endpoint allows users to store an image file into the database.

        Example usage with curl:

        curl -X POST http://localhost:8000/api/store/ \\
          -H 'Content-Type: multipart/form-data' \\
          -F 'file=@/home/dev/Downloads/test_image.jpg'

        Explanation of the curl command:
        - `-X POST`: Specifies the HTTP method as POST, indicating that data will be submitted to the server.
        - `http://localhost:8000/api/store/`: The URL of the API endpoint where the image will be uploaded.
        - `-H 'Content-Type: multipart/form-data'`: Specifies that the request body contains a multipart form for file upload.
        - `-F 'file=@/home/dev/Downloads/test_image.jpg'`: Adds a file field (`file`) to the form data being submitted.
          - Replace `/home/dev/Downloads/test_image.jpg` with the actual path to the image file on your local machine.

        Response:
        - Upon successful upload, the API will respond with a status code 201 (Created) and a JSON response indicating success:
          {
            "message": "Image stored successfully"
          }

        Notes:
        - Ensure that the Django server is running and accessible at `http://localhost:8000`.
        - Adjust the file path (`/home/dev/Downloads/test_image.jpg`) to match the location of the image file you wish to upload.
        - Verify permissions and file existence on the local machine before running the curl command.
        - Monitor the command-line output for any errors or warnings, and check Django server logs (`python manage.py runserver`) for additional information.
        """

        file_obj = request.FILES['file']

        if file_obj:
            # Save the file to MEDIA_ROOT
            file_path = Path(settings.MEDIA_ROOT, file_obj.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file_obj.chunks():
                    destination.write(chunk)

            # Create Image model instance with image name and current date/time
            image_instance = Image.objects.create(
                image=file_obj.name
            )

            # Manually set the uploaded_at field
            image_instance.uploaded_at = datetime.now()
            image_instance.save()
            return Response({'message': 'Image stored successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No file found in request'}, status=status.HTTP_400_BAD_REQUEST)
