from django.urls import path

from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('posts/', views.all_posts, name='all_posts'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('about/', views.about, name='about'),
]
