from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('news/', views.article_list, name='article-list'),
    path('news/<slug:slug>/', views.article_detail, name='article-detail'),
    path('news/category/<slug:slug>/', views.category_view, name='category'),
    path('htmx/ministry-tabs/', views.ministry_tabs, name='ministry-tabs'),
]
