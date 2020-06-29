from django.db import models
from django.conf import settings
import random

User=settings.AUTH_USER_MODEL

class Tweet(models.Model):
    user=models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    content=models.TextField(blank=True, null=True)
    image=models.FileField(upload_to='images/', blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-created',)

    def serialize(self):
        return {
            'id':self.id,
            'content':self.content,
            'likes':random.randint(0, 180)
        }