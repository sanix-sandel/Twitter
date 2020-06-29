from django.db import models
import random

class Tweet(models.Model):
    content=models.TextField(blank=True, null=True)
    image=models.FileField(upload_to='images/', blank=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-created',)

    def serialize(self):
        return {
            'id':self.id,
            'content':self.content,
            'likes':random.randint(0, 180)
        }