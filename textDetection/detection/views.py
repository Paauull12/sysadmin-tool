from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ImageUploadSerializer
from .text_detection_soft import functionThatParsesThePicture
from rest_framework.parsers import MultiPartParser, FormParser


class ImgProcessor(APIView):
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('image_with_password')

        # Verificăm dacă fișierul a fost primit
        if not file_obj:
            return Response({'error': 'No file found in request'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Logica ta pentru procesarea fișierului
            username, password = functionThatParsesThePicture(file_obj)
            return Response(
                {
                    'username': username,
                    'password': password,
                },
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            # Loghează excepția pentru debugging
            print(f"Error: {e}")
            return Response({'error': "An error occurred while processing the image." + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)