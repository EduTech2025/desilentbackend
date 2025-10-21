# desilentbackend/urls.py (project-level)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),         # Django admin site
    path('api/users/', include('users.urls')),     # API routes for users app: /api/...
    path('api/contacts/', include('contact.urls')),   # all contact APIs start with /api/contact/
  ]
