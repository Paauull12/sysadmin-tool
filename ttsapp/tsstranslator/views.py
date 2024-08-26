from rest_framework.views import APIView
from rest_framework.response import Response
from gtts import gTTS
from io import BytesIO
from django.http import HttpResponse

class TextProcessor(APIView):

    def post(self, request, *args, **kwargs):
        text = request.data.get('text')

        if not text:
            return Response({"detail": "Text is required."}, status=401)

        tts = gTTS(text)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)  

        return HttpResponse(audio_bytes, content_type='audio/mpeg')
