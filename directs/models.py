from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max


# Create your models here.
class Message(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        sender = self.sender
        recipient = self.recipient
        return f'from {sender} to {recipient}'

    def send_message(from_user, to_user, title, body):
        #보낸 사람의 메세지
        message = Message(
            #user=from_user,
            sender=from_user,
            recipient=to_user,
            title=title,
            body=body,
            )
        message.save()

        #받은 사람의 메세지
        # recipient_message = Message(
        #     #user=to_user,
        #     sender=from_user,
        #     body=body,
        #     recipient=to_user, )
        # recipient_message.save()
        return message

    def get_messages(user):
        messages = Message.objects.filter(user=user).values('recipient').annotate(last=Max('date')).order_by('-last')
        users = []
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['recipient']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()
            })
        return users
