# Create your models here.

from datetime import date
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse

import uuid # Required for unique book instances

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    email = models.EmailField()
    designation = models.CharField(max_length=100)
    commends = models.IntegerField()
    replies = models.IntegerField()

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

class Post(models.Model):
    """Model representing a post on the forum. This post could be an original post or a reply."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this post')
    title = models.CharField(max_length=500)

    TOPICS = (
        ('m', 'Maintenance'),
        ('o', 'Tankers'),
        ('a', 'Suez Max'),
        ('r', 'Engine Room'),
    )

    topic = ArrayField(models.CharField(max_length=200, choices=TOPICS), blank=True)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Otherwise this would have been a ManyToMany field.
    # Author is a string rather than an object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    date_posted = models.DateTimeField(null=True, blank=True, auto_now=True)
    contents = models.CharField(null=True, blank=True)
    commends = models.IntegerField(null=True, blank=True, default=0)
    replies = models.IntegerField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the URL to access a particular post."""
        return reverse('post-detail', args=[str(self.id)])    


    class Meta:
        ordering = ['date_posted']

    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'

def ready():
    from django.contrib.auth.models import User
    user = User.objects.create_user('myusername',
                                    'myemail@crazymail.com',
                                    'mypassword')
    user.first_name = 'Tyrone'
    user.last_name = 'Citizen'
    user.save()
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

