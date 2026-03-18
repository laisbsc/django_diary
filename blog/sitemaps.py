from django.contrib.sitemaps import Sitemap
from django.utils import timezone

from .models import Post


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        # Returns all published posts ordered by most recent
        return Post.objects.filter(
            published_date__lte=timezone.now()
        ).order_by('-published_date')

    def lastmod(self, obj):
        # updated_at reflects the last time the post was saved
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()
