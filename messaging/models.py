from django.db import models
from datetime import datetime

# Create your models here.
# django creates id fields for us automatically, so we don't need to 
# add one
class CustomUser(models.Model):
    username = models.CharField(max_length=100, default="")
    password = models.CharField(max_length=100, default="")

    def __str__(self):
        return "Username: %s, id %d" %(self.username, self.id)

class Message(models.Model):
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