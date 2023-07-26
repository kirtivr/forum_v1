from typing import Any, Dict
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger(__name__)

# Create your views here.
#from .models import Book, Author, BookInstance, Genre

from django.views import generic
from .models import Post
from django.template import Context, Template
from django.template.loader import render_to_string

def index(request):
    num_books = 10
    num_instances = 30 #BookInstance.objects.all().count()
    num_instances_available = 364 #BookInstance.objects.filter(status__exact='a').count()
    fiction_genres = 735 #Genre.objects.all().filter(name__contains='fiction').exclude(name__contains='non').count()
    summer_theme_titles = 54128 #Book.objects.all().filter(title__icontains='Summer').count()
    num_authors = 0 #Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    sk = request.session.keys()
    session = request.session.items()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'fiction_genres': fiction_genres,
        'summer_theme_titles': summer_theme_titles,
        'session': session,
        'header': render_to_string('headers/header.html'),
        'sidebar': render_to_string('sidebars/index.html'),
        'posts': render_to_string('posts/post_list_item.html',
                                  context = {'posts': Post.objects.all()})
    }

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