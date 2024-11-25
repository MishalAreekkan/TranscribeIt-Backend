from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadTranscription,TextTranscription
from .serializer import UploadTranscriptionSerializer,TextTranscriptionSerializer
from Project.utils import transcribe_audio  # Import transcribe_audio function from utils


class TextTranscriptionView(APIView):
    def get(self, request):
        transcriptions = TextTranscription.objects.all().order_by('-created_at')
        serializer = TextTranscriptionSerializer(transcriptions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TextTranscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class TranscriptionAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """
        GET method to retrieve a transcription by ID or filter by user.
        """
        transcription_id = request.query_params.get('id', None)
        user_id = request.query_params.get('user_id', None)

        # If an ID is provided, retrieve that specific transcription
        if transcription_id:
            try:
                transcription = UploadTranscription.objects.get(id=transcription_id)
                serializer = UploadTranscriptionSerializer(transcription)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except UploadTranscription.DoesNotExist:
                return Response({"error": "Transcription not found."}, status=status.HTTP_404_NOT_FOUND)

        # If a user_id is provided, retrieve transcriptions for that user
        elif user_id:
            transcriptions = UploadTranscription.objects.filter(user_id=user_id)
            if transcriptions.exists():
                serializer = UploadTranscriptionSerializer(transcriptions, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No transcriptions found for this user."}, status=status.HTTP_404_NOT_FOUND)

        # If no filter is provided, return all transcriptions
        else:
            transcriptions = UploadTranscription.objects.all()
            serializer = UploadTranscriptionSerializer(transcriptions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
    def post(self, request):
        # Check if the audio file exists in the request
        audio_file = request.FILES.get('audio_file')
        if not audio_file:
            return Response({"error": "No audio file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Log file details for debugging (consider using logging instead of print in production)
        print(f"Received file: {audio_file.name}, Type: {audio_file.content_type}")

        try:
            # Use the utility function to transcribe the audio file
            transcript = transcribe_audio(audio_file)

            # Save transcription in the database
            transcription = UploadTranscription.objects.create(audio_file=audio_file, transcript=transcript)
            serializer = UploadTranscriptionSerializer(transcription)

            # Return the serialized data as the response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # Log the error (consider using logging in production)
            print(f"Error: {str(e)}")
            return Response({"error": "Can't translate the uploaded audio, please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
