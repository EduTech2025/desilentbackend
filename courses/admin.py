from django.contrib import admin
from .models import Course, Session, Comment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'duration', 'created_at', 'update_on', 'updated_by')
    search_fields = ('course_name', 'updated_by')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_name', 'course', 'session_index', 'release_date', 'start_time', 'end_time', 'updated_by')
    list_filter = ('course',)
    search_fields = ('session_name', 'updated_by')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'ratings', 'session', 'course', 'created_at')
    list_filter = ('ratings', 'course')
    search_fields = ('user_name', 'email', 'comment')
