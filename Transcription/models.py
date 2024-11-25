from django.db import models
from django.contrib.auth.models import User


class TextTranscription(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transcription {self.id} - {self.created_at}"
    
    
class UploadTranscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    audio_file = models.FileField(upload_to='audio_files/', null=True, blank=True) 
    transcript  = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)        

    def __str__(self):
        return f"Transcription {self.id} - {self.user if self.user else 'Anonymous'}"



