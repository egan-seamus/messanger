from django.test import TestCase

# Create your tests here.

from messaging.models import CustomUser, Message 
from datetime import datetime
from django.db.models import Q
from django.core.serializers import serialize

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

    def test_message_from_same_conversation(self):
        user3 = CustomUser.objects.create(username="a", password="b")
        messageOneTwo = Message.objects.create(sender=self.user1, recipient=self.user2, text="test message", timestamp=datetime.now())
        messageTwoOne = Message.objects.create(sender=self.user2, recipient=self.user1, text="test message", timestamp=datetime.now())
        messageOneThree = Message.objects.create(sender=self.user1, recipient=user3, text="test message", timestamp=datetime.now())
        messageOneOne = Message.objects.create(sender=self.user1, recipient=self.user1, text="test message", timestamp=datetime.now())
        self.assertTrue(messageOneTwo.isFromSameConversation(messageTwoOne))
        self.assertFalse(messageOneTwo.isFromSameConversation(messageOneThree))
        self.assertFalse(messageOneOne.isFromSameConversation(messageOneThree))
        self.assertTrue(messageOneOne.isFromSameConversation(messageOneOne))

    def test_filtering_previews(self):
        user3 = CustomUser.objects.create(username="a", password="b")
        messageOneTwo = Message.objects.create(sender=self.user1, recipient=self.user2, text="test message", timestamp=datetime.now())
        messageTwoOne = Message.objects.create(sender=self.user2, recipient=self.user1, text="test message", timestamp=datetime.now())
        messageOneThree = Message.objects.create(sender=self.user1, recipient=user3, text="test message", timestamp=datetime.now())
        messageOneOne = Message.objects.create(sender=self.user1, recipient=self.user1, text="test message", timestamp=datetime.now())

        messages = Message.objects.all()
        #allSent = Message.objects.filter(sender__id=request.session.['id']).order_by('timestamp')
        uniqueMessages = [messages[0]]
        for unfilteredEntry in messages:
            unique = True
            for filteredEntry in uniqueMessages:
                if(unfilteredEntry.isFromSameConversation(filteredEntry)):
                    unique = False
            if unique:
                uniqueMessages.append(unfilteredEntry)

        jason = serialize("json", uniqueMessages);
        print(jason)
        # there are 3 unique conversations right now 
        # 1 to 1 
        # 1 to 2
        # 1 to 3
        self.assertEqual(len(uniqueMessages), 3)
        
