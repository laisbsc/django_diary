import logfire
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import About, Category, Post


def post_list(request):
    with logfire.span('post list'):
        with logfire.span('fetch featured post'):
            published = Post.objects.filter(
                published_date__lte=timezone.now()
            ).order_by('-published_date')
            featured_post = (
                published.filter(is_featured=True).first()
                or published.first()
            )

        with logfire.span('fetch posts'):
            posts = list(published)

    return render(request, 'blog/list.html', {
        'posts': posts,
        'featured_post': featured_post,
        'blog_tagline': getattr(settings, 'BLOG_TAGLINE', ''),
    })


def post_detail(request, slug):
    with logfire.span('post detail', slug=slug):
        with logfire.span('fetch post', slug=slug):
            post = get_object_or_404(Post, slug=slug)

        with logfire.span('fetch recent posts'):
            recent_posts = list(
                Post.objects
                .filter(published_date__lte=timezone.now())
                .exclude(pk=post.pk)
                .order_by('-published_date')[:4]
            )

        with logfire.span('fetch categories'):
            categories = list(Category.objects.all())

    return render(request, 'blog/detail.html', {
        'post': post,
        'recent_posts': recent_posts,
        'categories': categories,
    })


def all_posts(request):
    with logfire.span('all posts'):
        with logfire.span('fetch posts'):
            posts = list(
                Post.objects.filter(published_date__lte=timezone.now())
                .order_by('-published_date')
                .select_related('category', 'author')
            )
    return render(request, 'blog/all_posts.html', {'posts': posts})


def about(request):
    about_page = About.objects.filter(pk=1).first()
    return render(request, 'blog/about.html', {'about': about_page})
