from django.urls import path, include, re_path
import django.contrib.auth.views
from . import views

urlpatterns = [
    path('', views.index, name='posts'),
    path('new', views.new_post_view, name='new'),
    re_path('^(?P<filter_by>[\w-]+)', views.filter_posts, name='filter_posts_by'),
]