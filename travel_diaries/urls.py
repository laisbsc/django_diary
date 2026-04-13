from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView

from blog.sitemaps import BlogSitemap

sitemaps = {'blog': BlogSitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('map/', include('map.urls')),
    path('ai/', include('ai_tools.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
