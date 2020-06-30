from django.urls import path
from . import views

urlpatterns=[
 #   path('', views.tweets_list, name='home'),
    path('action/', views.tweet_action),
    path('create-tweet/', views.tweet_create, name='create-tweet'),
    path('<int:tweet_id>/', views.tweet_detail),
    path('<int:tweet_id>/delete/', views.tweet_delete),
]