# desilentbackend/urls.py (project-level)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),         # Django admin site
    path('api/users/', include('users.urls')),     # API routes for users app: /api/...
    path('blogger/', include('blogs.urls')),  # API routes for blogs app: /api/blogs/...       # all user APIs start with /api/users/
    path('api/contact/', include('contact.urls')),   # all contact APIs start with /api/contact/
    path('api/courses/', include('courses.urls')), 
    path('api/pdf/', include('modules.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('', include('myapp.urls')),
]
