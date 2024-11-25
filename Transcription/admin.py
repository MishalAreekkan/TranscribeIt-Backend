from django.contrib import admin
from . models import TextTranscription,UploadTranscription
# Register your models here.

admin.site.register(TextTranscription)
admin.site.register(UploadTranscription)

# superuser
# name-admin
# email-admin@gmail.com
# password-admin
