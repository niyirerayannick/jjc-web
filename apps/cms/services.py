"""Shared query helpers for editorial article surfaces."""
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Article, Category


def ministry_feed_context(request):
    """Build the filtered, paginated homepage ministry newsletter context."""
    category_slug = request.GET.get('ministry_category', 'all')
    articles = (
        Article.objects
        .filter(status='published', published_date__lte=timezone.now())
        .select_related('category', 'author')
        .order_by('-is_featured', '-published_date', '-created_at')
    )

    if category_slug != 'all':
        articles = articles.filter(category__slug=category_slug)

    paginator = Paginator(articles, 20)
    page_obj = paginator.get_page(request.GET.get('ministry_page', 1))
    page_articles = list(page_obj.object_list)

    categories = (
        Category.objects
        .filter(is_active=True)
        .order_by('order', 'name')
    )

    from apps.advertising.models import AdCampaign
    ministry_sidebar_ads = list(
        AdCampaign.objects
        .filter(
            status='active',
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date(),
            position__slug='homepage-ministry-sidebar',
        )
        .select_related('position')
        .order_by('?')[:2]
    )

    return {
        'ministry_category': category_slug,
        'ministry_categories': categories,
        'ministry_page_obj': page_obj,
        'ministry_featured': page_articles[0] if page_articles else None,
        'ministry_secondary_feature': page_articles[1] if len(page_articles) > 1 else None,
        'ministry_left_feed': page_articles[2:7],
        'ministry_right_feed': page_articles[7:12],
        'ministry_latest_feed': page_articles[1:8],
        'ministry_more_feed': page_articles[8:12],
        'ministry_top_stories': page_articles[1:3],
        'ministry_updates': page_articles[3:10],
        'ministry_community': page_articles[16:20],
        'ministry_sidebar_ads': ministry_sidebar_ads,
    }
