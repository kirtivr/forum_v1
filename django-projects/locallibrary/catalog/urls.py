from django.urls import path
from . import views

urlpatterns = [
    # name = index is recognized by the URL mapper.
    # <a href="{% url 'index' %}">Home</a>.
    # Redirects to the views.index function.

    # It is more robust than <a href="/catalog/">Home</a>
    # because we could change the pattern for our webpage (this is external facing).
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    # Note int is optional, and 'pk' is whatever is passed to book/* forwarded to the detail view.
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]