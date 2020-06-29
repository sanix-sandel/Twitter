from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Tweet

def home(request):
    qs=Tweet.objects.all()
    tweets=[{"id":x.id, 'content':x.content} for x in qs]
    data={
        'response':tweets
    }
    return render(request, 'pages/home.html', (data))

def tweets_list(request):
    qs=Tweet.objects.all()
    tweets=[{"id":x.id, 'content':x.content} for x in qs]
    data={
        'response':tweets
    }
    return JsonResponse(data)

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