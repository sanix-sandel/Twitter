from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Tweet

# Create your views here.
def tweet_detail(request, tweet_id, *args, **kwargs):
    try:
        obj=Tweet.objects.get(id=tweet_id)
    except:
        raise Http404
    data={
        'id':tweet_id,
        'content':obj.content
    }
    return JsonResponse(data)