from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post


def post_list(request):
    published = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    # Featured: first post with is_featured=True, fallback to latest.
    # is_featured field added in Phase 2 — getattr guards against AttributeError.
    featured_post = next(
        (p for p in published if getattr(p, 'is_featured', False)),
        published.first()
    )

    return render(request, 'blog/list.html', {
        'posts': published,
        'featured_post': featured_post,
        # TODO: move to a context processor once BLOG_TAGLINE is stable
        'blog_tagline': getattr(settings, 'BLOG_TAGLINE', 'AI · Community · Human things'),
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    recent_posts = (
        Post.objects
        .filter(published_date__lte=timezone.now())
        .exclude(pk=pk)
        .order_by('-published_date')[:4]
    )

    # Category model added in Phase 2 — guard import so the view doesn't crash now.
    try:
        from .models import Category
        categories = Category.objects.all()
    except Exception:
        categories = []

    return render(request, 'blog/detail.html', {
        'post': post,
        'recent_posts': recent_posts,
        'categories': categories,
    })
