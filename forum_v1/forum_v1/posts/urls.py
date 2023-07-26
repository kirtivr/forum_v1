from django.urls import path, include, re_path
import django.contrib.auth.views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_post_view, name='new'),
]