from django.db import models
from django.contrib.auth.models import User

from icontext import settings


class Chat(models.Model):
    created = models.DateTimeField()
    #TODO использовать uuid вместо имени
    title = models.TextField(max_length=512, unique=True)
    is_active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, verbose_name='User')

    def __str__(self):
        return f'{self.title} - {self.created}'


class ChatMessages(models.Model):
    sended = models.DateTimeField()
    title = models.TextField(max_length=512)
    body = models.TextField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')

    def __str__(self):
        return f'{self.title} - {self.sended} - {self.user.username}'
