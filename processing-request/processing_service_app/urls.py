from django.urls import path

from processing_service_app.views import ImageVisualizationView

urlpatterns = [
    path('view/', ImageVisualizationView.as_view(), name='image_view'),
]
