from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('tweets/', views.tweets_list, name='tweets_list'),
    path('<int:tweet_id>/', views.tweet_detail, name='tweet'),
    path('create-tweet/', views.tweet_create_view, name='create-tweet'),
]