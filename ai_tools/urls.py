from django.urls import path

from . import views

urlpatterns = [
    path('generate-image/', views.generate_image_view, name='generate_image'),
    path('gallery/', views.image_gallery_view, name='image_gallery'),
    path('gallery/<int:pk>/', views.image_detail_view, name='image_detail'),
]
