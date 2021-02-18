from django.db import models
from datetime import datetime

# Create your models here.
class CustomUser(models.Model):
    user_id = models.BigIntegerField(default=0) 
    username = models.CharField(max_length=100, default="")
    password = models.CharField(max_length=100, default="")

    def __str__(self):
        return "Username: %s, Hashed Password %s, user_id %d" %(self.username, self.password, self.user_id)

class Message(models.Model):
    #TODO FIX THIS
    message_id = models.BigIntegerField
    sender = models.ForeignKey(CustomUser, 
                               null=True, 
                               on_delete=models.SET_NULL,
                               related_name="sender")
    recipient = models.ForeignKey(CustomUser, 
                                  null=True, 
                                  on_delete=models.SET_NULL,
                                  related_name="recipient")
    text = models.CharField(max_length=5000, default="")
    timestamp = models.DateTimeField(default=datetime.fromisoformat('1970-01-01'))