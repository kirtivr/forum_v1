from typing import Any, Dict
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger(__name__)

# Create your views here.
from .models import Book, Author, BookInstance, Genre

from django.views import generic

class BookListView(generic.ListView):
    # These are all keywords, similar to "context" in index below.
    model = Book
    paginate_by = 1
    context_object_name = 'book_list'   # your own name for the list as a template variable
    queryset = Book.objects.all()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # Call the base implementation first to get the context.
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

from django.contrib.auth.decorators import login_required
class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    # These are all keywords, similar to "context" in index below.
    model = Author
    paginate_by = 1
    context_object_name = 'author_list'   # your own name for the list as a template variable
    queryset = Author.objects.all()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # Call the base implementation first to get the context.
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

from django.contrib.auth.decorators import permission_required

#@permission_required('catalog.can_mark_returned', raise_exception=True)
class AllBorrowedBooksListView(generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o')
            .order_by('due_back')
        )

@permission_required('catalog.can_mark_returned', raise_exception=True)
def mark_book_returned(request):
    book_id = request.GET.get('id')
    book_inst = BookInstance.objects.get(id__exact=book_id)
    logger.exception('book status = %s', str(book_inst.status))
    book_inst.due_back = None
    book_inst.borrower = None
    book_inst.status = 'a'
    book = book_inst.book
    book_inst.save()
    return redirect('/catalog/book/'+str(book.id))

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    fiction_genres = Genre.objects.all().filter(name__contains='fiction').exclude(name__contains='non').count()
    summer_theme_titles = Book.objects.all().filter(title__icontains='Summer').count()
    num_authors = Author.objects.count()
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
    }

    return render(request, 'index.html', context=context)

def logout_view(request):
    logout(request)
    return render(request,template_name='registration/logged_out.html')

import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Post request, user has submitted the form.
    if request.method == 'POST':
        # Create a form instance, populating it with data from the request.
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))

    # Get request, user is trying to get the empty form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')