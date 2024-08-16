from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from .models import Image
from .serializers import ImageSerializer

class ImageVisualizationView(APIView):
    def get(self, request):
        try:
            # Retrieve the latest image from the database
            latest_image = Image.objects.latest('uploaded_at')

            # Serialize the image data
            serializer = ImageSerializer(latest_image)

            # Return only the serialized data (body)
            return JsonResponse(serializer.data)

        except Image.DoesNotExist:
            # Handle the case where no images exist in the database
            return JsonResponse({"error": "No images found"}, status=status.HTTP_404_NOT_FOUND)
