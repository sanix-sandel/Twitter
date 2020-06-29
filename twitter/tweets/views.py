from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm

def home(request):
    qs=Tweet.objects.all()
    tweets=[{"id":x.id, 'content':x.content} for x in qs]
    data={
        'response':tweets
    }
    return render(request, 'pages/home.html', (data))

def tweet_create_view(request, *args, **kwargs):
    form=TweetForm(request.POST or None)
    if form.is_valid():
        obj=form.save(commit=False)
        obj.save()
        form=TweetForm()
    return render(request, 'components/form.html', {'form':form})    

def tweets_list(request):
    qs=Tweet.objects.all()
    tweets=[{"id":x.id, 'content':x.content} for x in qs]
    data={
        'isUser':False,
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