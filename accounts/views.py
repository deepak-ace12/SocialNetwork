from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from home.models import Post, Friend
from accounts.forms import (
    RegistrationForm,
    UserEditForm
)

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from accounts.models import UserProfile


def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('home:home'))
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)


def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    posts = Post.objects.all().order_by('-created')
    userpost = Post.objects.filter(user=user).order_by('-created')
    args = {'user': user, 'posts':posts, 'userpost': userpost, }
    return render(request, 'accounts/profile.html', args)


def edit_profile(request):
    print(request.user.username)
    if request.method == 'POST':
        user = UserProfile.objects.get(user=request.user)
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        return redirect(reverse('accounts:view_profile'))
    else:
        user = UserProfile.objects.get(user=request.user)
        form = UserEditForm(instance=user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)


'''    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

'''
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


def view_connections(request, pk=None, action=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    friend, created = Friend.objects.get_or_create(current_user=request.user)
    if action == 'followers':
        connected_people = friend.followers.all()
    elif action == 'following':
        connected_people = friend.following.all()

    followers = friend.followers.all()
    following = friend.following.all()
    userpost = Post.objects.filter(user=user).order_by('-created')
    args = {
        'user': user, 'connected_people': connected_people, 'userpost': userpost,
        'followers': followers, 'following': following,
    }
    return render(request, 'accounts/connections.html', args)
