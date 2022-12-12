from rest_framework import serializers
from .models import ImageMaster

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageMaster
        fields = ('name', 'image')