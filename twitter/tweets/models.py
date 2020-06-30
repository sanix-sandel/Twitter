from django.db import models
from django.conf import settings
import random

User=settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    tweet=models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
    parent=models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    user=models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    content=models.TextField(blank=True, null=True)
    likes=models.ManyToManyField(User, related_name='tweets_liked', blank=True)
    image=models.FileField(upload_to='images/', blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-created',)

    @property
    def is_retweet(self):
        return self.parent!=None    

    def serialize(self):
        return {
            'id':self.id,
            'content':self.content,
            'likes':random.randint(0, 180)
        }

    def __str__(self):
        return f'{self.content}'    