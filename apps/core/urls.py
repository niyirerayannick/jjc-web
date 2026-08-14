from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('mission-vision/', views.mission_vision, name='mission-vision'),
    path('about/academy/', views.content_page, {'slug': 'academy'}, name='academy'),
    path('about/legacy/', views.content_page, {'slug': 'legacy'}, name='legacy'),
    path('about/future/', views.content_page, {'slug': 'future'}, name='future'),
    path('committee/', views.committee, name='committee'),
    path('partners/', views.partners_page, name='partners'),
    path('search/', views.search, name='search'),
    path('robots.txt', views.robots_txt, name='robots-txt'),
]
