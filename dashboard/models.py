from tarfile import NUL
from django.db import models

class Message(models.Model):
    sender_id = models.TextField(null=True, blank=True)
    receiver_id = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"From {self.sender_id} to {self.receiver_id} - {self.message[:20]}"
