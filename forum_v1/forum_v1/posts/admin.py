from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance

class AuthorInstanceInline(admin.TabularInline):
    model = Author
    extra = 0

class BooksInline(admin.TabularInline):
    model = Book
    extra = 0

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    # will display horizontally if you further group them in a tuple (as shown in the "date" fields below)
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    inlines = [BooksInline]

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BooksInstanceInline]

# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)