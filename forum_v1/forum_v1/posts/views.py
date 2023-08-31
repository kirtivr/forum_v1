from typing import Any, Dict
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger(__name__)

# Create your views here.
#from .models import Book, Author, BookInstance, Genre

from django.views import generic
from .models import Post, Reply, Author, search_posts_and_replies
from django.template import Context, Template
from django.template.loader import render_to_string

from django.core.paginator import Paginator
def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    sk = request.session.keys()
    session = request.session.items()
    all_posts = Post.objects.all()
    search_query = None
    if request.GET:
        search_query = request.GET.get('q')
        if search_query:
            all_post_ids = search_posts_and_replies(search_query)
            #logger.warn(f'all post_ids = {all_post_ids}')         	
            all_posts = Post.objects.filter(id__in=all_post_ids)

    paginator = Paginator(all_posts, 4)
    page_number = request.GET.get("page") if request.GET.get("page") else 0
    page_obj = paginator.get_page(page_number)

    #logger.warn(f'page_obj = {page_obj} number = {page_obj.number} page_obj.previous_page_number = {page_obj.previous_page_number} next = {page_obj.next_page_number}')
    context = {
        'session': session,
        'posts': render_to_string('posts/post_list_item.html',
                                  context = {'page_obj': page_obj}),
        'search_query': search_query if search_query else "", 'page_obj': page_obj
    }

    return render(request, 'index.html', context=context)

def filter_posts(request, filter_by):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    session = request.session.items()
    all_posts = Post.objects.all()
    if filter_by == 'latest_activity':
        all_posts = Post.objects.order_by('-latest_activity')
    elif filter_by == 'new_posts':
        all_posts = Post.objects.order_by('-date_posted')
    elif filter_by == 'unanswered':
        ordered_replies = Reply.objects.order_by('-date_posted')
        posts = set()
        for reply in ordered_replies:
            if reply.original_post not in posts:
                posts.add(reply.original_post)
        all_posts = list(set(all_posts).difference(posts))

    search_query = None
    if request.GET:
        search_query = request.GET.get('q')
        if search_query:
            all_post_ids = search_posts_and_replies(search_query)
            #logger.warn(f'all post_ids = {all_post_ids}')         	
            all_posts = filter(lambda post : True if post.id in all_post_ids else False, all_posts)

    paginator = Paginator(all_posts, 4)
    page_number = request.GET.get("page") if request.GET.get("page") else 0
    page_obj = paginator.get_page(page_number)

    context = {
        'session': session,
        'posts': render_to_string('posts/post_list_item.html',
                                  context = {'page_obj': page_obj},
                                  request=request),
        'search_query': search_query if search_query else "", 'page_obj': page_obj}
    
    return render(request, 'index.html', context=context)

def handle_uploaded_file(f, destination_url):
    os.makedirs(os.path.dirname(destination_url), exist_ok=True)

    with open(destination_url, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def handle_added_files(cleaned_data, new_post):
    for i in range(len(cleaned_data)):
        destination_url = os.path.join(uploaded_files_path(new_post.id), cleaned_data[i].name)
        if not new_post.file_paths:
            new_post.file_paths = [cleaned_data[i].name]
        else:
            new_post.file_paths.append(cleaned_data[i].name)
        handle_uploaded_file(cleaned_data[i], destination_url)

from django.template import RequestContext
def post_detail(request, post_id):
    def handle_new_reply(form, new_reply, request):
        new_reply.author=request.user.author
        new_reply.contents=form.cleaned_data['reply']
        if form.cleaned_data['file_field']:
            handle_added_files(form.cleaned_data['file_field'], new_reply)

    # Fetch the post.
    post = Post.objects.get(id=post_id)
    # Reply added.
    if request.method == "POST":
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():
            new_reply = Reply()
            new_reply.original_post = post
            post.latest_activity = new_reply.date_posted
            handle_new_reply(form, new_reply, request)
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
import os
from django.db.models import FilePathField
from .models import uploaded_files_path
@login_required
def new_post_view(request):
    def handle_new_post(form, new_post, request):
        current_user = request.user
        current_author = current_user.author
        new_post.author = current_author
        new_post.title =  form.cleaned_data['title']
        new_post.contents = form.cleaned_data['new_post']
        new_post.commends = 0
        new_post.num_replies = 0
        new_post.topic = form.cleaned_data['topics']
        if form.cleaned_data['file_field']:
            handle_added_files(form.cleaned_data['file_field'], new_post)

    form = None
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = Post()
            handle_new_post(form, new_post, request)
            new_post.save()
            return HttpResponseRedirect(
                reverse('posts')
            )
        else:
            form = NewPostForm()     
    else:
        form = NewPostForm()

    return render(request, template_name="posts/new_post.html",
                context={"form": form})

def download_attachment(request, post_id, file_name):
    file_path = os.path.join(uploaded_files_path(post_id), file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read())
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404

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
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy