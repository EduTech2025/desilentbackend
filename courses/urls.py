from django.urls import path
from courses.views.course_view import CourseView
from courses.views.session_view import SessionView
from courses.views.comment_view import CommentView
from courses.views.project_view import ProjectSubmissionAPI


from courses.views.feedback_view import FeedbackView

urlpatterns = [
    path('course/', CourseView.as_view(), name='course-aditya'),
    path('session/', SessionView.as_view(), name='session-api'),
    path('comments/', CommentView.as_view(), name='comment-api'),
    path('projects/', ProjectSubmissionAPI.as_view(), name='project-api'),
    path('feedbacks/', FeedbackView.as_view(), name='feedback-api'),
]
