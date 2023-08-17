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
    if not Author.objects.filter(user=instance):
        Author.objects.create(user=instance)
    instance.author.save()

class AbstractReply(models.Model):
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, related_name="reply_author")
    original_post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="reply_to_post")

    class Meta:
        abstract = True

import os
from forum_v1.settings import STATIC_URL
def uploaded_files_path(post_id):
    return os.path.join(STATIC_URL, "assets", "uploads")

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

def ready():
    pass

# Create a new record using the model's constructor.
#record = MyModelName(my_field_name="Instance #1")

# Save the object into the database.
#record.save()

# Access model field values using Python attributes.
#print(record.id) # should return 1 for the first record.
#print(record.my_field_name) # should print 'Instance #1'

# Change record by modifying the fields, then calling save().
#record.my_field_name = "New Instance Name"
#record.save()

#all_books = Book.objects.all()

# can also be:
# icontains (case insensitive), iexact (case-insensitive exact match), exact (case-sensitive exact match) and in, gt (greater than), startswith, etc

#wild_books = Book.objects.filter(title__contains='wild')
#number_wild_books = wild_books.count()

