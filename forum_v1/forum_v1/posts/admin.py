from django.contrib import admin

# Register your models here.

from .models import Author, Post

class AuthorInstanceInline(admin.TabularInline):
    model = Author
    extra = 0

class PostsInline(admin.TabularInline):
    model = Post
    extra = 0

# Define the admin class
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'display_name', 'email', 'designation', 'commends', 'replies')

    # will display horizontally if you further group them in a tuple (as shown in the "date" fields below)
    fields = ['last_name', 'first_name', 'display_name', 'email', 'designation', ('commends', 'replies')]

    inlines = [PostsInline]

class PostsInline(admin.TabularInline):
    model = Post
    extra = 0

# Register the Admin classes for Post using the decorator
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'topic', 'contents', 'commends', 'num_replies')