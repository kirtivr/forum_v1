from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
#from rest_framework import routers, serializers, viewsets
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('', RedirectView.as_view(url='posts/', permanent=True)),
]

# Use static() to add URL mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)