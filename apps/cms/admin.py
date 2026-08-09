from django.contrib import admin
from .models import Article, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'is_featured', 'published_date', 'views')
    list_filter = ('status', 'category', 'is_featured')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status', 'is_featured')
    date_hierarchy = 'published_date'
    fieldsets = (
        ('Content', {'fields': ('title', 'slug', 'category', 'author', 'featured_image',
                                'featured_image_alt', 'excerpt', 'content')}),
        ('Media', {'fields': ('video_url', 'youtube_url', 'tags')}),
        ('Publishing', {'fields': ('status', 'published_date', 'is_featured', 'allow_comments')}),
        ('SEO', {'fields': ('seo_title', 'seo_description', 'seo_image', 'canonical_url'),
                 'classes': ('collapse',)}),
    )
