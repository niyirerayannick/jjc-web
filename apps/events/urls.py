from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event-list'),
    path('live/', views.live_stream_page, name='live'),
    path('imana-iratsinze/', views.imana_iratsinze, name='imana-iratsinze'),
    path('<slug:slug>/', views.event_detail, name='event-detail'),
]
