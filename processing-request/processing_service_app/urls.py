from django.urls import path

from processing_service_app.views import ImageUploadView

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='image_upload'),
]
