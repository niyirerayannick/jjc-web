from django.urls import path
from . import views

app_name = 'ministry'

urlpatterns = [
    path('testimonies/', views.testimonies, name='testimonies'),
    path('testimonies/share/', views.share_testimony, name='share-testimony'),
    path('evangelization/', views.evangelization, name='evangelization'),
]
