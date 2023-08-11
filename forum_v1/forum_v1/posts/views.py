from typing import Any, Dict
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger(__name__)

# Create your views here.
#from .models import Book, Author, BookInstance, Genre

from django.views import generic
from .models import Post, Reply, Author
from django.template import Context, Template
from django.template.loader import render_to_string

def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    sk = request.session.keys()
    session = request.session.items()

    context = {
        'session': session,
        #'header': render_to_string('headers/header.html'),
        #'sidebar': render_to_string('sidebars/new_sidebar.html'),
        'posts': render_to_string('posts/post_list_item.html',
                                  context = {'posts': Post.objects.all()})
    }

    return render(request, 'index.html', context=context)

def filter_posts(request, filter_by):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    session = request.session.items()

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
        #'header': render_to_string('headers/header.html', {}, request=request),
        #'sidebar': render_to_string('sidebars/new_sidebar.html', {},  request=request),
        'posts': render_to_string('posts/post_list_item.html', context = {'posts': all_posts}, request=request)}
    
    return render(request, 'index.html', context=context)

from django.template import RequestContext
def post_detail(request, post_id):
    # Fetch the post.
    post = Post.objects.get(id=post_id)
    # Reply added.
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            new_reply = Reply.objects.create(original_post=post, author=request.user.author, contents=form.cleaned_data['reply'])
            new_reply.save()
            post = Post.objects.get(id=post_id)
            context = {
                'session': request.session.items(),
                'post': post,
                'reply': render_to_string('posts/reply_post.html', request=request, context={'reply_form': ReplyForm()})
            }
            return render(request, 'posts/post_detail.html', context=context)
        else:
            # Unexpected, log something here.
            pass
    context = {
        'session': request.session.items(),
        'post': post,
        'reply': render_to_string('posts/reply_post.html', request=request, context={'reply_form': ReplyForm()})
    }
    return render(request, 'posts/post_detail.html', context=context)

from .forms import NewPostForm, ReplyForm
from django.contrib.auth.decorators import login_required
@login_required
def new_post_view(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            new_post = Post()
            current_user = request.user
            current_author = current_user.author
            new_post.author = current_author
            new_post.title =  form.cleaned_data['title']
            new_post.contents = form.cleaned_data['new_post']
            new_post.commends = 0
            new_post.num_replies = 0
            new_post.topic = form.cleaned_data['topics']
            new_post.save()
            return HttpResponseRedirect(
                reverse('posts')
            )
    else:
        form = NewPostForm()
        return render(request, template_name="posts/new_post.html",
                    context={"form": form})

from django.views import generic
class author_detail(generic.DetailView):
    model = Author

    def get_object(self, queryset=None):
        return Author.objects.get(id=self.kwargs.get("author_id"))

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