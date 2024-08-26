from django.urls import path
from .views import TextProcessor

urlpatterns = [
    path('listen/', TextProcessor.as_view(), name="main-listen"),
]