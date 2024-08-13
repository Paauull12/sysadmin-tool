from django.urls import path
from django.views.generic import TemplateView

from .views import ImageUploadAPI

urlpatterns = [
    path('store/', ImageUploadAPI.as_view(), name='image_upload_api'),
    path('upload/', TemplateView.as_view(template_name='upload_form.html'), name='upload_form'),
]
