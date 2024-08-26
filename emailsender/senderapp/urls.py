from django.urls import path, include
from .views import EmailSender

urlpatterns = [
    path('send-mail/', EmailSender.as_view(), name='send-email'),
]

