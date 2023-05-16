from django.urls import path, include, re_path
import django.contrib.auth.views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.post_list_view, name='new'),
    path('books/', views.BookListView.as_view(), name='books'),
    # Note int is optional, and 'pk' is whatever is passed to book/* forwarded to the detail view.
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('book-return/', views.mark_book_returned, name='book-return'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-books'),
    path('all-borrowed/', views.AllBorrowedBooksListView.as_view(), name='all-borrowed'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]