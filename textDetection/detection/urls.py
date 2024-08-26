from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  ImgProcessor

router = DefaultRouter()
router.register(r'process-image', ImgProcessor.as_view(), basename="process-image")

urlpatterns = [
    #path('', include(router.urls)),
    path('process-image/', ImgProcessor.as_view(), name='process-image'),
]

