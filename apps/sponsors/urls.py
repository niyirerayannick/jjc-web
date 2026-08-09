from django.urls import path
from . import views

app_name = 'sponsors'

urlpatterns = [
    path('become-a-sponsor/', views.become_sponsor, name='become-sponsor'),
    path('portal/', views.sponsor_portal, name='portal'),
]
