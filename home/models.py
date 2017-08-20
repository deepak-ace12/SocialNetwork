from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    post = models.TextField(max_length=160)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    re_tweets = models.IntegerField(default=0)

    def __str__(self):
        return self.post


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)


class Retweets(models.Model):
    current_post = models.ForeignKey(Post, related_name='user_post', null= True)
    retweeters = models.ManyToManyField(User)
    @classmethod
    def retweet_positive(cls, current_user, current_post):
        retweet_by, created = cls.objects.get_or_create(
            current_post=current_post
        )
        retweet_by.retweeters.add(current_user)

    @classmethod
    def retweet_negative(cls, current_user, retweeter):
        retweet_by, created = cls.objects.get_or_create(
            current_user=current_user
        )
        retweet_by.retweeters.remove(retweeter)



