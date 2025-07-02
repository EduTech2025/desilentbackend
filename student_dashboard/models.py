from django.db import models

class Message(models.Model):
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    message = models.TextField()
    timestamp = models.DateTimeField()
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"From {self.sender_id} to {self.receiver_id} - {self.message[:20]}"
