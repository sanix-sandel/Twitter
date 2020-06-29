from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm

def home(request):
    qs=Tweet.objects.all()
    tweets=[x.serialize() for x in qs]
    data={
        'response':tweets
    }
    return render(request, 'pages/home.html', (data))

def tweet_create_view(request, *args, **kwargs):
    form=TweetForm(request.POST or None)
    next_url=request.POST.get('next') or None
    if form.is_valid():
        obj=form.save(commit=False)
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) #201==created items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
                
        form=TweetForm()
    return render(request, 'components/form.html', {'form':form})    

def tweets_list(request):
    qs=Tweet.objects.all()
    tweets=[x.serialize() for x in qs]
    data={
        'isUser':False,
        'response':tweets
    }
    return JsonResponse(data)

# Create your views here.
def tweet_detail(request, tweet_id, *args, **kwargs):
    data={
        'id':tweet_id,
    }
    status=200
    try:
        obj=Tweet.objects.get(id=tweet_id)
        data['content']=obj.content
    except:
        data['message']='Not found'
        status=404
    
    return JsonResponse(data, status=status)#json.dumps content_type='application/json'