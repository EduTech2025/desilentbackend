from django.urls import path
from . import views

urlpatterns = [
    # Course URLs
    path('courses/', views.course_list_create),
    path('courses/<uuid:course_id>/', views.course_detail),

    # Session URLs
    path('sessions/', views.session_list_create),
    path('sessions/<uuid:session_id>/', views.session_detail),

    # Comment URLs
    path('comments/', views.comment_list_create),
    path('comments/<uuid:comment_id>/', views.comment_detail),
]
