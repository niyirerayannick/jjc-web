from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),

    # Articles
    path('articles/', views.articles, name='articles'),
    path('articles/new/', views.article_create, name='article-create'),
    path('articles/<int:pk>/edit/', views.article_edit, name='article-edit'),
    path('articles/<int:pk>/delete/', views.article_delete, name='article-delete'),
    path('categories/', views.categories, name='categories'),

    # Music
    path('music/albums/', views.albums, name='albums'),
    path('music/albums/new/', views.album_form, name='album-create'),
    path('music/albums/<int:pk>/edit/', views.album_form, name='album-edit'),
    path('music/songs/', views.songs, name='songs'),
    path('music/songs/new/', views.song_form, name='song-create'),
    path('music/songs/<int:pk>/edit/', views.song_form, name='song-edit'),

    # Events
    path('events/', views.events, name='events'),
    path('events/new/', views.event_form, name='event-create'),
    path('events/<int:pk>/edit/', views.event_form, name='event-edit'),
    path('events/livestreams/', views.livestreams, name='livestreams'),
    path('events/livestreams/new/', views.livestream_form, name='livestream-create'),
    path('events/livestreams/<int:pk>/edit/', views.livestream_form, name='livestream-edit'),

    # Gallery
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/albums/new/', views.gallery_album_form, name='gallery-album-create'),
    path('gallery/albums/<int:pk>/edit/', views.gallery_album_form, name='gallery-album-edit'),
    path('gallery/albums/<int:pk>/media/', views.gallery_album_media, name='gallery-album-media'),

    # Sponsors
    path('sponsors/applications/', views.sponsor_applications, name='sponsor-applications'),
    path('sponsors/applications/<int:pk>/', views.sponsor_application_detail, name='sponsor-application-detail'),
    path('sponsors/groups/', views.sponsor_groups, name='sponsor-groups'),

    # Advertising
    path('advertising/campaigns/', views.ad_campaigns, name='ad-campaigns'),
    path('advertising/packages/', views.ad_packages, name='ad-packages'),

    # Messages
    path('messages/', views.messages_list, name='messages'),
    path('messages/<int:pk>/', views.message_detail, name='message-detail'),

    # Newsletter
    path('newsletter/', views.newsletter_subscribers, name='newsletter'),

    # Media
    path('media/', views.media_library, name='media-library'),
    path('media/upload/', views.upload_media, name='upload-media'),
    path('media/upload-tinymce/', views.upload_tinymce_image, name='upload-tinymce'),

    # Settings
    path('settings/', views.site_settings, name='settings'),
    path('content/', views.content_hub, name='content-hub'),
    path('content/<str:kind>/new/', views.content_edit, name='content-create'),
    path('content/<str:kind>/<int:pk>/edit/', views.content_edit, name='content-edit'),

    # Slider
    path('slider/', views.slider, name='slider'),
    path('slider/new/', views.slider_form, name='slider-create'),
    path('slider/<int:pk>/edit/', views.slider_form, name='slider-edit'),
    path('slider/<int:pk>/delete/', views.slider_delete, name='slider-delete'),

    # Committee & Partners
    path('committee/', views.committee, name='committee'),
    path('partners/', views.partners, name='partners'),

    # Reports
    path('reports/', views.reports, name='reports'),
]
