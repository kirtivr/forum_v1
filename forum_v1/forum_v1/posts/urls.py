from django.urls import path, include, re_path
import django.contrib.auth.views
from . import views

urlpatterns = [
    path('', views.index, name='posts'),
    path('new', views.new_post_view, name='new'),
    path('post-detail/<uuid:post_id>/', views.post_detail, name='post-detail'),
    path('author-detail/<int:author_id>/', views.author_detail.as_view(), name='author-detail'),
    re_path('^(?P<filter_by>[\w-]+)', views.filter_posts, name='filter_posts_by'),
]