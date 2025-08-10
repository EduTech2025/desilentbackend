import uuid
from django.db import models

from users.models import CustomUser


# from course.models.course_model import CustomUser

class Course(models.Model):
    course_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_name = models.CharField(max_length=255,null=True, blank=True)
    duration = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    img_url = models.URLField(max_length=500,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.course_name
    
class Session(models.Model):
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    session_name = models.CharField(max_length=255,null=True, blank=True)
    session_url = models.URLField(max_length=500,null=True, blank=True)
    session_index = models.PositiveIntegerField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    img_url = models.URLField(max_length=500,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return f"{self.session_name} (Course: {self.course.course_name})"
    
class Comment(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    ratings = models.PositiveSmallIntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.ratings}★"
    

class ProjectSubmission(models.Model):
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project_id = models.CharField(max_length=100, unique=True)
    project_name = models.CharField(max_length=255,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    technologies = models.CharField(max_length=255,null=True, blank=True)
    github_link = models.URLField(blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return f"{self.project_name} by {self.student.username}"


class Feedback(models.Model):
    feedback_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100,null=True, blank=True)
    updated_by = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return f"{self.student_id} - {self.message[:30]}"





    
