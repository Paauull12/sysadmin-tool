from rest_framework import serializers


class ImageUploadSerializer(serializers.Serializer):
    image_path = serializers.CharField(max_length=255)
