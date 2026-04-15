from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from blog.sitemaps import BlogSitemap

sitemaps = {'blog': BlogSitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('map/', include('map.urls')),
    path('ai/', include('ai_tools.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
