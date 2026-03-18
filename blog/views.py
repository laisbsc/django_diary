from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import About, Category, Post


def post_list(request):
    published = Post.objects.filter(
        published_date__lte=timezone.now()
    ).order_by('-published_date')

    featured_post = (
        published.filter(is_featured=True).first()
        or published.first()
    )

    return render(request, 'blog/list.html', {
        'posts': published,
        'featured_post': featured_post,
        'blog_tagline': getattr(settings, 'BLOG_TAGLINE', ''),
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    recent_posts = (
        Post.objects
        .filter(published_date__lte=timezone.now())
        .exclude(pk=post.pk)
        .order_by('-published_date')[:4]
    )

    return render(request, 'blog/detail.html', {
        'post': post,
        'recent_posts': recent_posts,
        'categories': Category.objects.all(),
    })


def about(request):
    about_page = About.objects.filter(pk=1).first()
    return render(request, 'blog/about.html', {'about': about_page})
