from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
# from rest_framework import routers, serializers, viewsets
from django.views.generic import RedirectView


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('sentry-debug/', trigger_error),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('posts/', include('posts.urls')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='posts/', permanent=True)),
]

# Use static() to add URL mapping to serve static files during development (only)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
