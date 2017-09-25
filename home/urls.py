from django.conf.urls import url
from home.views import HomeView
from . import views
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends'),
    url(r'^retweet/(?P<action>.+)/(?P<pk>\d+)/$', views.retweet, name='retweet'),
    url(r'^retweet-profile/(?P<action>.+)/(?P<pk>\d+)/$', views.retweet_profile, name='retweet_profile'),
    url(r'^like/(?P<action>.+)/(?P<pk>\d+)/$', views.likes, name='like'),

]