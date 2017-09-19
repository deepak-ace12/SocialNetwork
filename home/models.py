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
    following = models.ManyToManyField(User, related_name='following')
    followers = models.ManyToManyField(User, related_name='followers')
    current_user = models.ForeignKey(User, related_name='owner', null=True)

    def __str__(self):
        return str(self.current_user)


    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )

        recent_friend, created = cls.objects.get_or_create(
            pk=new_friend.pk, current_user=new_friend
        )

        friend.following.add(new_friend)
        recent_friend.followers.add(current_user)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        recent_friend, created = cls.objects.get_or_create(
            pk=new_friend.pk, current_user=new_friend
        )

        friend.following.remove(new_friend)
        recent_friend.followers.remove(current_user)

class Retweets(models.Model):
    current_post = models.ForeignKey(Post, related_name='user_post', null=True)
    retweeters = models.ManyToManyField(User)
    posted_by = models.ForeignKey(User, related_name='post_owner', null=True)

    def __str__(self):
        return str(self.current_post)


    @classmethod
    def retweet_positive(cls, current_user, current_post):
        retweet_by, created = cls.objects.get_or_create(
            current_post=current_post, posted_by = current_post.user
        )
        retweet_by.retweeters.add(current_user)



    @classmethod
    def retweet_negative(cls, current_user, current_post):
        retweet_by, created = cls.objects.get_or_create(
            current_post=current_post
        )
        retweet_by.retweeters.remove(current_user)



