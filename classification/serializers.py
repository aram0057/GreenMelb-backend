from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    uploaded_file = serializers.ImageField()
