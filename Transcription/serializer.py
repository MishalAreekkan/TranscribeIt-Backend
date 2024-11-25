from rest_framework import serializers
from .models import UploadTranscription,TextTranscription

class UploadTranscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadTranscription
        fields = ['id', 'user', 'audio_file', 'transcript', 'created_at']
        

class TextTranscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextTranscription
        fields = '__all__'
