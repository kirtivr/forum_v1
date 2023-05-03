from django.urls import path
from . import views

urlpatterns = [
    # name = index is recognized by the URL mapper.
    # <a href="{% url 'index' %}">Home</a>.
    # Redirects to the views.index function.

    # It is more robust than <a href="/catalog/">Home</a>
    # because we could change the pattern for our webpage (this is external facing).
    path('', views.index, name='index'),
]