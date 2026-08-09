from django.urls import path
from . import views

app_name = 'advertising'

urlpatterns = [
    path('advertise-with-us/', views.advertise, name='advertise'),
    path('track/<int:campaign_id>/', views.track_impression, name='track'),
]
