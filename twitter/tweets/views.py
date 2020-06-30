import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .forms import TweetForm
from .models import Tweet
from django.contrib.auth.decorators import login_required

from .serializers import TweetSerializer
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, 
    permission_classes,
    authentication_classes
)  
from rest_framework.authentication import SessionAuthentication  
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import (
    TweetSerializer, 
    TweetActionSerializer,
    TweetCreateSerializer
)



def home(request):
    qs=Tweet.objects.all()
    tweets=[x.serialize() for x in qs]
    data={
        'tweets':tweets
    }
    return render(request, 'pages/home.html', (data))


@api_view(['POST'])
#@authentication_classes([Sessionauthentication])
@permission_classes([IsAuthenticated])
def tweet_create(request, *args, **kwargs):
    print('life')
    serializer=TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        print('life is')
        return Response(serializer.data, status=201)
    return Response({}, status=400)    


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete(request, tweet_id, *args, **kwargs):
    qs=Tweet.objectsfilter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs=qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message":"You cannot delete this tweet"}, status=404)
    obj=qs.first()
    obj.delete()
    #serializer=TweetSerializer(obj)
    return Response({"message":"tweet removed"}, status=200)        

@api_view(['GET'])
def tweets_list(request, *args, **kwargs):
    qs=Tweet.objects.all()
    serializer=TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def tweet_detail(request, tweet_id, *args, **kwargs):
    qs=Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj=qs.first()
    serializer=TweetSerializer(obj)    
    return Response(serializer.data, status=200)   


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action(request, *args, **kwargs):
    #id required
   
    serializer=TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data=serializer.validated_data
        tweet_id=data.get("id")
        action=data.get("action")
        print(action)
        qs=Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj=qs.first()
        content=obj.content
        print(content)
        if action=="like":
            obj.likes.add(request.user)
            serializer=TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action=="unlike":
            obj.likes.remove(request.user)
            serializer=TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action=='retweet':
            print(content)
            new_tweet=Tweet.objects.create(
                user=request.user,
                parent=obj,
                content=content
            )            
            serializer=TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
    return Response({}, status=200)        


def like_tweet(request, *args, **kwargs):
    qs=Tweet.objectsfilter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj=qs.first()
    if request.user in obj.likes.all():
        obj.likes.remove(request.user)
        return Response({"message":"You cannot delete this tweet"}, status=404)
    
    return Response({"message":"tweet removed"}, status=200)  