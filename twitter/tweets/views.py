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


def home(request):
    qs=Tweet.objects.all()
    tweets=[x.serialize() for x in qs]
    data={
        'response':tweets
    }
    return render(request, 'pages/home.html', (data))


@api_view(['POST'])
#@authentication_classes([Sessionauthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    
    serializer=TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)    


@login_required
def tweet_create(request, *args, **kwargs):
    form=TweetForm(request.POST or None)
    next_url=request.POST.get('next') or None
    if form.is_valid():
        obj=form.save(commit=False)
        obj.user=request.user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) #201==created items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
                
        form=TweetForm()
    if form.errors:
        if request.is_ajax():#make sure it's ajax request
            return JsonResponse(form.errors, status=400)    
    return render(request, 'components/form.html', {'form':form})    

@api_view(['GET'])
def tweets_list(request):
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