from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('<slug:slug>/', views.album_gallery, name='album-gallery'),
]
