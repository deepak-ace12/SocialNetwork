from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    post = models.TextField(max_length=160)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    retweeters = models.ManyToManyField(User, related_name='retweeters')
    likers = models.ManyToManyField(User, related_name='likers')

    def __str__(self):
        return self.post

    @classmethod
    def retweet_positive(cls, current_user, current_post):
        retweet_by, created = cls.objects.get_or_create(
            post=current_post, user=current_post.user
        )
        retweet_by.retweeters.add(current_user)

    @classmethod
    def retweet_negative(cls, current_user, current_post):
        retweet_by, created = cls.objects.get_or_create(
            post=current_post
        )
        retweet_by.retweeters.remove(current_user)

    @classmethod
    def like_positive(cls, current_user, current_post):
        liked_by, created = cls.objects.get_or_create(
            post=current_post, user=current_post.user
        )
        liked_by.likers.add(current_user)


    @classmethod
    def like_negative(cls, current_user, current_post):
        liked_by, created = cls.objects.get_or_create(
            post=current_post
        )
        liked_by.likers.remove(current_user)


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
