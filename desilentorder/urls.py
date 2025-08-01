# desilentbackend/urls.py (project-level)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),         # Django admin site
    path('api/', include('users.urls')),     # API routes for users app: /api/...
    path('blogger/', include('blogs.urls')),  # API routes for blogs app: /api/blogs/...
    path('api/', include('contact.urls')),
    path('api/', include('courses.urls')),
    path('pdf/', include('modules.urls')),
    path('student-dash/', include('student_dashboard.urls')),
    path('', include('myapp.urls')),
]
