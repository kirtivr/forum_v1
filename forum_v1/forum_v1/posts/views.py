from typing import Any, Dict
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger(__name__)

# Create your views here.
#from .models import Book, Author, BookInstance, Genre

from django.views import generic
from .models import Post, Reply
from django.template import Context, Template
from django.template.loader import render_to_string

def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    sk = request.session.keys()
    session = request.session.items()

    context = {
        'session': session,
        'header': render_to_string('headers/header.html'),
        'sidebar': render_to_string('sidebars/new_sidebar.html'),
        'posts': render_to_string('posts/post_list_item.html',
                                  context = {'posts': Post.objects.all()})
    }

    return render(request, 'index.html', context=context)

def filter_posts(request, filter_by):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    sk = request.session.keys()
    session = request.session.items()

    post_context = None
    if filter_by == 'latest_activity':
        all_posts = Post.objects.order_by('latest_reply')
    elif filter_by == 'new_posts':
        all_posts = Post.objects.order_by('date_posted')
    elif filter_by == 'best':
        all_posts = Post.objects.order_by('commends')
    elif filter_by == 'unanswered':
        ordered_replies = Reply.objects.order_by('post_date')
        posts = set()
        for reply in ordered_replies:
            if reply.original_post not in posts:
                posts.add(reply.original_post)
        all_posts = list(posts)

    context = {
        'session': session,
        'header': render_to_string('headers/header.html', {}, request=request),
        'sidebar': render_to_string('sidebars/new_sidebar.html', {},  request=request),
        'posts': render_to_string('posts/post_list_item.html', context = {'posts': all_posts}, request=request)}
    
    return render(request, 'index.html', context=context)

def new_post_view(request):
    return render(request, template_name="posts/new_post.html")

def logout_view(request):
    logout(request)
    return render(request,template_name='registration/logged_out.html')

def post_list_view(request):
    return render(request, template_name='posts/post_list_item.html')

import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy