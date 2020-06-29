from django.urls import path
from . import views

urlpatterns=[
    path('<int:tweet_id>/', views.tweet_detail, name='tweet'),
]