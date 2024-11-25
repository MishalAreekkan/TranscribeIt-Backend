import requests
from django.conf import settings

def transcribe_audio(audio_file):
    # Deepgram API setup
    deepgram_api_url = "https://api.deepgram.com/v1/listen"
    headers = {
        "Authorization": f"Token {settings.DEEPGRAM_API_KEY}",
    }
    files = {
        'file': (audio_file.name, audio_file.read(), audio_file.content_type),
    }

    # Make the API call to Deepgram for transcription
    response = requests.post(deepgram_api_url, headers=headers, files=files)
    
    if response.status_code == 200:
        # Extract the transcript from the API response
        transcript = response.json().get('results', {}).get('channels', [{}])[0].get('alternatives', [{}])[0].get('transcript', '')
        return transcript
    else:
        raise Exception(f"Failed to transcribe audio. Deepgram API returned {response.status_code}: {response.text}")
