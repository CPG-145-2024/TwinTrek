from rest_framework import serializers
from .models import WebcamImage

class WebcamImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebcamImage
        fields = '__all__'
