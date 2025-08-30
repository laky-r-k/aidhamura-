from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Add this field to track if a message has been read
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'From {self.sender.username} to {self.receiver.username} at {self.timestamp:%Y-%m-%d %H:%M}'

    class Meta:
        ordering = ('timestamp',)
