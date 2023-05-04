from typing import Any, Dict
from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre

from django.views import generic

class BookListView(generic.ListView):
    # These are all keywords, similar to "context" in index below.
    model = Book
    context_object_name = 'book_list'   # your own name for the list as a template variable
    queryset = Book.objects.all() # Get 5 books containing the title war

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # Call the base implementation first to get the context.
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(generic.DetailView):
    model = Book
    
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    fiction_genres = Genre.objects.all().filter(name__contains='fiction').exclude(name__contains='non').count()
    summer_theme_titles = Book.objects.all().filter(title__icontains='Summer').count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'fiction_genres': fiction_genres,
        'summer_theme_titles': summer_theme_titles,
    }

    return render(request, 'index.html', context=context)