from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from home.forms import HomeForm
from home.models import Post, Friend
from django.contrib.auth.models import User

class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        form = HomeForm()
        posts = Post.objects.all().order_by('-created')
        users = User.objects.exclude(id=request.user.id)
        user = User.objects.get(id=request.user.id)
        friend, created = Friend.objects.get_or_create(current_user=request.user)
        following = friend.following.all()
        followers = friend.followers.all()
        userpost = Post.objects.filter(user=user).order_by('-created')
        args = {
            'form': form, 'posts': posts,
            'users': users, 'following': following,
            'followers': followers,
            'userpost': userpost,
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            text = form.cleaned_data['post']
            form = HomeForm()
            return redirect('home:home')

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)


def change_friends(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, new_friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, new_friend)
    return redirect('home:home')


def retweet(request, action, pk):
    post = Post.objects.get(pk=pk)
    if action == 'positive':
        Post.retweet_positive(request.user, post)
    elif action == 'negative':
        Post.retweet_negative(request.user, post)
    return redirect('home:home')


def retweet_profile(request, action, pk):
    post = Post.objects.get(pk=pk)
    if action == 'positive':
        Post.retweet_positive(request.user, post)
    elif action == 'negative':
        Post.retweet_negative(request.user, post)
    return redirect('accounts:view_profile')


def likes(request, action, pk):
    post = Post.objects.get(pk=pk)
    if action == 'positive':
        Post.like_positive(request.user, post)
    elif action == 'negative':
        Post.like_negative(request.user, post)
    return redirect('home:home')