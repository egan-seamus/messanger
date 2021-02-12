from django.db import models

# Create your models here.
class CustomUser(models.Model):
    user_id = models.BigIntegerField(default=0) 
    username = models.CharField(max_length=100, default="")
    password = models.CharField(max_length=100, default="")

class Message(models.Model):
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