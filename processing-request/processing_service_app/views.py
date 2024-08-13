import os
import shutil

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer

from pathlib import Path
from .utils.shell import run


from .utils.image_processing import resize_images_to_a4
from processing_service import settings

from processing_service.settings import TOOLS_PATH

class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        """
        API Endpoint for Image Upload and Processing.

        Accepts a POST request with a JSON payload containing the path to an image file.
        The image is then processed through various image processing functions.

        Example Request using curl:

            curl -X POST -H "Content-Type: application/json" \\
                 -d '{"image_path": "/home/dev/Downloads/test_image.jpg"}' \\
                 http://127.0.0.1:8000/api/upload/

        Replace '/home/dev/Downloads/test_image.jpg' with the actual path to the image file you want to upload and process.

        Returns a JSON response indicating the status of the image processing:

            {
                "message": "Image uploaded and processed successfully."
            }

        In case of an error or invalid request, appropriate HTTP status codes and error messages are returned.

        Note:
        - Ensure that the API endpoint (`/api/upload/`) is accessible and the Django server is running.
        - The image processing involves orientation detection, image straightening, resizing to A4 dimensions, and binarization.
        - No authorization is needed
        """
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image_path = serializer.validated_data['image_path']
            image_name_without_extension = Path(image_path).stem

            if not os.path.exists(image_path):
                return Response({'error': 'File not found'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the directory if it doesn't exist
            if not os.path.exists(settings.TARGET_DIR):
                os.makedirs(settings.TARGET_DIR)

            if os.path.exists(settings.TARGET_DIR / image_name_without_extension):
                shutil.rmtree(settings.TARGET_DIR / image_name_without_extension)
            os.makedirs(settings.TARGET_DIR / image_name_without_extension)

            # Copy the image to the TARGET_DIR
            save_path = settings.TARGET_DIR / image_name_without_extension / Path(image_path).name
            shutil.copy(image_path, save_path)

            # Reorient Images
            run(
                [
                    Path(TOOLS_PATH) / "detectOrientation" / "detectOrientation",
                    settings.TARGET_DIR / image_name_without_extension,
                    settings.TARGET_DIR / image_name_without_extension / "oriented",
                    settings.TARGET_DIR / image_name_without_extension / "oriented",
                ]
            )


            # Resize pdf pages to normal A4
            resize_images_to_a4(settings.TARGET_DIR / image_name_without_extension / "oriented" / "straighten_up")


            return Response({'message': 'Image uploaded and processed successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
