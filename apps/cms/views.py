from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article, Category


def article_list(request):
    category_slug = request.GET.get('category')
    articles = Article.objects.filter(status='published').select_related('category', 'author')

    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug, is_active=True)
        articles = articles.filter(category=active_category)

    categories = Category.objects.filter(is_active=True)
    paginator = Paginator(articles, 12)
    page = paginator.get_page(request.GET.get('page'))

    if request.htmx:
        return render(request, 'cms/partials/article_cards.html', {
            'articles': page,
            'page_obj': page,
        })

    return render(request, 'cms/article_list.html', {
        'articles': page,
        'page_obj': page,
        'categories': categories,
        'active_category': active_category,
        'page_title': 'News & Updates',
        'breadcrumb': [('Home', '/'), ('News', '')],
    })


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    article.increment_views()

    related = (
        Article.objects
        .filter(status='published', category=article.category)
        .exclude(pk=article.pk)
        .order_by('-published_date')[:3]
    )

    return render(request, 'cms/article_detail.html', {
        'article': article,
        'related_articles': related,
        'page_title': article.get_seo_title(),
        'seo_description': article.get_seo_description(),
    })


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    articles = Article.objects.filter(status='published', category=category).select_related('author')
    paginator = Paginator(articles, 12)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'cms/article_list.html', {
        'articles': page,
        'page_obj': page,
        'active_category': category,
        'categories': Category.objects.filter(is_active=True),
        'page_title': category.name,
        'breadcrumb': [('Home', '/'), ('News', '/news/'), (category.name, '')],
    })


def ministry_tabs(request):
    """HTMX endpoint for the homepage ministry newsletter."""
    from .services import ministry_feed_context
    return render(request, 'cms/partials/ministry_newsletter.html', ministry_feed_context(request))
