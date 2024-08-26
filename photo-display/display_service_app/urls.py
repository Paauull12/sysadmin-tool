from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.image_list, name='image_list'),
    path('api/<int:image_id>/', views.image_retrieve, name="image-retrieve")
]