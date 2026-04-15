from django.urls import path

from . import views

urlpatterns = [
    path('generate-image/', views.generate_image_view, name='generate_image'),
    path('generate-image/<int:pk>/pending/', views.image_pending_view, name='image_pending'),
    path('generate-image/<int:pk>/status/', views.image_status_view, name='image_status'),
    path('gallery/<int:pk>/delete/', views.image_delete_view, name='image_delete'),
    path('gallery/', views.image_gallery_view, name='image_gallery'),
    path('gallery/<int:pk>/', views.image_detail_view, name='image_detail'),
]
