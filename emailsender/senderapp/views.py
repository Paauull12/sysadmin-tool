from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import base64

#axvj sluw ogoh mfma

class EmailSender(APIView):

    def post(self, request, *args, **kwargs):
        
        smtp_server="smtp.gmail.com"
        smtp_port=587
        sender = request.data.get('sender')
        receiver = request.data.get('receiver')
        text = request.data.get('text')
        password = request.data.get('password')

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = text[:min(10, len(text) - 1)]

        msg.attach(MIMEText(text, 'plain'))

        # Check if there is an audio file in the request
        audio_file = request.FILES.get('audio')
        if audio_file:
            # Crează un atașament din fișierul audio
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(audio_file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{audio_file.name}"')
            msg.attach(part)
            
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg)

                return Response({'success': "email was sent"}, status=status.HTTP_200_OK)
        except Exception as e:
                return Response({'error': 'not really good request tbh :)'}, status=status.HTTP_400_BAD_REQUEST)