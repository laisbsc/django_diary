from django.urls import path

from . import views

urlpatterns = [
    path('generate-image/', views.generate_image_view, name='generate_image'),
]
