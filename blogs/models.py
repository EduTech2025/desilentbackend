from django.db import models

class BlogDescription(models.Model):
    subheading = models.CharField(max_length=255)
    paragraph = models.TextField()
    images = models.JSONField(default=list)  # Storing list of image URLs or paths

class Blog(models.Model):
    header_image = models.URLField(blank=True)
    heading = models.CharField(max_length=255)
    description = models.ManyToManyField(BlogDescription, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    blog_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.heading

