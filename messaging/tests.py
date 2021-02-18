from django.test import TestCase

# Create your tests here.

from messaging.models import CustomUser, Message 
from datetime import datetime
from django.db.models import Q

class MessageTestCase(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(username="u", password="p")
        self.user2 = CustomUser.objects.create(username="b", password="v")
        Message.objects.create(sender=self.user1, recipient=self.user2, text="test message", timestamp=datetime.now())
        Message.objects.create(sender=self.user2, recipient=self.user1, text="test message", timestamp=datetime.now())
    
    def test_message_filtering(self):
        self.assertEqual(len(Message.objects.filter(Q(sender__id=self.user1.id) | Q(recipient__id=self.user1.id))), 2)
        self.assertEqual(len(Message.objects.filter(Q(sender__id=self.user1.id))), 1)
        self.assertEqual(len(Message.objects.filter(Q(recipient__id=self.user1.id))), 1)
