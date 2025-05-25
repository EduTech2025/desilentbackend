from django.db import models
import uuid

class Course(models.Model):
    course_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_name = models.CharField(max_length=255)
    duration = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255)

    def __str__(self):
        return self.course_name


class Session(models.Model):
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    session_name = models.CharField(max_length=255)
    session_url = models.URLField()
    session_index = models.PositiveIntegerField()
    release_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255)

    def __str__(self):
        return self.session_name


class Comment(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='comments')
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    ratings = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.comment[:20]}"
