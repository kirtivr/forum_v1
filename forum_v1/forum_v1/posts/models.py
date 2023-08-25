from datetime import date
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

import logging
logger = logging.getLogger(__name__)

import uuid # Required for unique book instances

class Author(models.Model):
    """Model representing an author."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    email = models.EmailField()
    designation = models.CharField(max_length=100)
    commends = models.IntegerField(null=True, blank=True, default=0)
    num_posts = models.IntegerField(null=True, blank=True, default=0)
    class Meta:
        ordering = ['last_name', 'first_name']

    def get_display_picture(self):
        """Returns the URI for the display picture for the author."""
        return ''

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'

@receiver(post_save, sender=User)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_author(sender, instance, **kwargs):
    logger.debug(f'instance = {instance}')
    try:
        if not Author.objects.filter(user=instance).exists() and Post.objects.count() >= 0:
            Author.objects.create(user=instance)
            instance.author.save()
    except:
        return

class AbstractReply(models.Model):
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, related_name="reply_author")
    original_post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="reply_to_post")

    class Meta:
        abstract = True

import os
from forum_v1.settings import STATICFILES_DIRS
def uploaded_files_path(post_id):
    return os.path.join(STATICFILES_DIRS[0], "assets", "uploads", str(post_id))

import posts.constants
class Post(models.Model):
    """Model representing a post on the forum. This post could be an original post or a reply."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this post')
    title = models.CharField(max_length=500)

    topic = ArrayField(models.CharField(max_length=200, choices=posts.constants.TOPICS_CHOICES), blank=True)

    # Foreign Key used because post can only have one author, but authors can have multiple posts.
    # Otherwise this would have been a ManyToMany field.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, related_name="author")
    date_posted = models.DateTimeField(null=True, blank=True, auto_now=True)
    latest_activity = models.DateTimeField(null=True, blank=True, auto_now=True)
    contents = models.CharField(max_length=10000, null=True, blank=True)
    commends = models.IntegerField(null=True, blank=True, default=0)
    num_replies = models.IntegerField(null=True, blank=True, default=0)
    file_paths = ArrayField(models.FilePathField(path=uploaded_files_path(id), default=None, null=True, blank=True))

    def get_absolute_url(self):
        """Returns the URL to access a particular post."""
        return reverse('post-detail', args=[str(self.id)])    

    class Meta:
        ordering = ['date_posted']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.title} by {self.author})'

class Reply(AbstractReply):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this post')

    date_posted = models.DateTimeField(null=True, blank=True, auto_now=True)
    contents = models.CharField(max_length=10000, null=True, blank=True)
    file_paths = ArrayField(models.FilePathField(path=uploaded_files_path(id), default=None, null=True, blank=True))

    #def get_absolute_url(self):
    #    """Returns the URL to access a particular post."""
    #    return reverse('post-detail', args=[str(self.id)])    

    class Meta:
        ordering = ['date_posted']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} by {self.author})'

def find_edit_distance(w1, w2):
    N = len(w1)
    M = len(w2)

    if N > M:
        w2 = w2 + (''.join(' ' for i in range(N - M)))
    else:
        w1 = w1 + (''.join(' ' for i in range(M - N)))

    grid = [[0 for i in range(max(M, N) + 1)] for j in range(max(M, N) + 1)]

    for i in range(1, max(M, N)):
        for j in range(1, max(M, N)):
            grid[i][j] = min(
                grid[i - 1][j - 1],
                grid[i - 1][j],
                grid[i][j - 1]
            )
            if w1[i - 1] != w2[j - 1]:
                grid[i][j] += 1

    return grid[max(M, N)][max(M, N)]

def score_number_of_in_order_words(match_indices):
    match_indices = list(filter(lambda idx : False if idx == None else True, match_indices))
    smi = sorted(match_indices)
    total_score = 0
    for i in range(len(match_indices)):
        if match_indices[i] == smi[i]:
            total_score += 2
    
    return total_score

def edit_distance_search_for_words(words, text):
    total_score = 0
    match_indices = []
    for word in words:
        word_score = 0
        matched_at = None
        for idx, text_word in enumerate(text):
            dist = find_edit_distance(word, text_word)
            if dist == 0:
                word_score = 3
                matched_at = idx
                break
            elif dist == 1:
                if word_score == 1:
                    word_score = 2
                    matched_at = idx
            elif dist == 2:
                if word_score == 0:
                    word_score = 1
                    matched_at = idx
        if word_score == 0:
            match_indices.append(None)
        else:
            match_indices.append(matched_at)
        total_score += word_score

    ordering_score = score_number_of_in_order_words(match_indices)
    return total_score + ordering_score

def search_posts_and_replies(search_query):
    # Return a sorted list of posts and replies which contain a full or partial match of the given search query.
    # An edit distance match, with dist = 0 gets 3 point.
    # An edit distance match, with dist = 1 gets 2 point.
    # An edit distance match, with dist = 2 gets 1 point.
    # Sort posts and reply texts with highest score and return them in order.

    # Ordering should also technically matter.
    # Not sure how much, but for now we give a +2 point per word if
    # order matches.
    posts = Post.objects.all()
    replies = Reply.objects.all()

    posts_score = {posts[i].id:0 for i in range(len(posts))}

    words = search_query.split()
    for i, post in enumerate(posts):
        score = edit_distance_search_for_words(words, post.contents)
        posts_score[post.id] = score

    for i, reply in enumerate(replies):
        score = edit_distance_search_for_words(words, reply.contents)
        posts_score[reply.original_post.id] = max(posts_score[reply.original_post.id], score)

    sorted_post_ids = [post_id for post_id, score in sorted(posts_score.items(), key=lambda item: item[1], reverse=True)]
    return list(filter(lambda post_id: True if posts_score[post_id] >= len(words) else False, sorted_post_ids))

def ready():
    pass