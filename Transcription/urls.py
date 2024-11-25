from django.urls import path
from .views import TranscriptionAPIView,TextTranscriptionView

urlpatterns = [
    path('TextTranscript/', TextTranscriptionView.as_view(), name='transcriptions'),
    path('UploadTranscribe/', TranscriptionAPIView.as_view(), name='transcribe'),
]