from django.contrib import admin
@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
   list_display = (
   'title', 'author', 'topic', 'contents'
   )


   inlines = [RepliesInline]
    model = Author

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'original_post', 'parent', 'date_posted')

@admin.register(Author)

class AuthorAdmin(admin.ModelAdmin):
# Register the Admin classes for Post using the decorator
    list_display = ['designation']
@admin.register(Post)
    extra = 0

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['designation']

    # will display horizontally if you further group them in a tuple (as shown in the "date" fields below)
    fields = ['designation']

    inlines = [PostsInline]

class PostsInline(admin.TabularInline):
    model = Post
    extra = 0

# Register the Admin classes for Post using the decorator
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'topic', 'contents')
