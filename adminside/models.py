from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)


class ReplyOnMessage(models.Model):
    msg = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='msg') # type: ignore
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_reply')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_reply')
    reply = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.reply

    class Meta:
        ordering = ('timestamp',)




    
