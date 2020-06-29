from rest_framework import serializers

from .models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tweet
        fields=('content',)

    def validate_content(self, value):
        if len(value)>240:
            raise serializers.ValidationError('This tweet is too long')     
        return value