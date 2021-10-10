from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.urls import reverse
from .models import BlingPost, BlingComment, BlingNotification
from copy import deepcopy
import datetime


def scan_for_forms(request):
    # like button has been pressed
    if request.POST.get('like'):
        liked_post_id = request.POST.get('like')
        liked_post = BlingPost.objects.get(pk=liked_post_id)

        # check if post is already liked by request.user
        liked_posts = request.user.profile.liked_posts.all()
        if liked_post in liked_posts:
            liked_post.likes_amount -= 1
            request.user.profile.liked_posts.remove(liked_post)
            liked_post.save()
            liked_post.author.profile.create_notification(request.user, 'больше не нравится ваш пост',
                                                          related_post=liked_post)
        else:
            liked_post.likes_amount += 1
            request.user.profile.liked_posts.add(liked_post)
            liked_post.save()
            liked_post.author.profile.create_notification(request.user, 'оценил(-а) ваш пост', related_post=liked_post)

    # comment has been left
    elif request.POST.get('comment_text'):
        comment_text = request.POST.get('comment_text')
        commented_post = BlingPost.objects.get(pk=request.POST.get('post_id'))
        new_comment = BlingComment(text=comment_text, author=request.user)
        new_comment.save()
        commented_post.comments.add(new_comment)
        commented_post.comments_amount = len(commented_post.comments.all())
        commented_post.save()
        if request.user != commented_post.author:
            commented_post.author.profile.create_notification(request.user, 'оставил(-а) комментарий под вашим постом',
                                                              related_post=commented_post)

    # new post has been created
    elif request.POST.get('new_post'):
        new_post = BlingPost(text=request.POST.get('new_post'), author=request.user)
        new_post.save()

    # subscribe button has been pressed
    elif request.POST.get('subscribe'):
        subscribant_user = User.objects.get(pk=request.POST.get('subscribe'))  # get user to be sub-ed to by his pk

        # get lists of sub-nt's subs&friends for some checks
        subscribant_subs = subscribant_user.profile.subscribers.all()
        subscribant_friends = subscribant_user.profile.friends.all()

        # now check if request.user is already sub-ed (or friended)
        if request.user in subscribant_subs or request.user in subscribant_friends:
            # user is already sub-ed
            # go to sub-nt page without any alerts
            return 0

        # now check if sub-nt is sub-ed to request.user (if true, they must become friends :з)
        if subscribant_user in request.user.profile.subscribers.all():
            # yep, he is, remove it...
            request.user.profile.subscribers.remove(subscribant_user)
            # ...to make them friends
            subscribant_user.profile.friends.add(request.user)
            request.user.profile.friends.add(subscribant_user)
            subscribant_user.profile.create_notification(request.user, 'подписался(-ась) на вас в ответ')
            return 0

        # not sub-ed, not friends, just a pure subscription
        subscribant_user.profile.subscribers.add(request.user)
        subscribant_user.profile.create_notification(request.user, 'подписался(-ась) на вас')

    # unsubscribe button has been pressed
    elif request.POST.get('unsubscribe'):
        subscribant_user = User.objects.get(pk=request.POST.get('unsubscribe'))  # get user to be unsub-ed by his pk

        # get lists of sub-nt's subs&friends for some checks
        subscribant_subs = subscribant_user.profile.subscribers.all()
        subscribant_friends = subscribant_user.profile.friends.all()

        # now check if request.user is unsub-ed
        if request.user not in subscribant_subs and request.user not in subscribant_friends:
            # user is already unsub-ed
            return 0

        # now check if sub-nt and request.user are friends
        if request.user in subscribant_friends:
            # yep, he is, unfriend them...
            subscribant_user.profile.friends.remove(request.user)
            request.user.profile.friends.remove(subscribant_user)
            # ...and just subscribe sub-nt to request.user
            request.user.profile.subscribers.add(subscribant_user)
            subscribant_user.profile.create_notification(request.user, 'и вы больше не друзья')
            return 0

        # not friends, request.user is just sub-ed to sub-nt, just pure unsubscription
        subscribant_user.profile.subscribers.remove(request.user)
        subscribant_user.profile.create_notification(request.user, 'отписался(-ась) от вас')

    # remove_post button has been pressed
    elif request.POST.get('remove_post'):
        post_to_delete = BlingPost.objects.get(pk=int(request.POST.get('remove_post')))
        if post_to_delete.author == request.user:
            for comment in post_to_delete.comments.all():
                comment.delete()
            post_to_delete.delete()

    # remove_comment button has been pressed
    elif request.POST.get('remove_comment'):
        comment_to_delete = BlingComment.objects.get(pk=int(request.POST.get('remove_comment').split('/')[1]))
        if comment_to_delete.author == request.user:
            comment_to_delete.delete()
            post = BlingPost.objects.get(pk=int(request.POST.get('remove_comment').split('/')[0]))
            post.comments_amount -= 1
            post.save()
            if request.user != post.author:
                post.author.profile.create_notification(request.user,
                                                        'удалил свой комментарий под вашим постом',
                                                        related_post=post)


def bling_signin(request):
    WELCOME_MESSAGE = 'Войдите в учетную запись'
    WRONG_LOGIN_OR_PASSWORD_MESSAGE = 'Неверное имя пользователя или пароль'
    DISABLED_USER_MESSAGE = 'Ошибка входа. Обратитесь к администратору сайта'
    if request.method == 'GET':
        return render(request, 'registration/login.html', {'greeting_message': WELCOME_MESSAGE})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # logged in, redirect to feed
                return redirect('/')
            else:
                return render(request, 'registration/login.html', {'greeting_message': DISABLED_USER_MESSAGE})
        else:
            return render(request, 'registration/login.html', {'greeting_message': WRONG_LOGIN_OR_PASSWORD_MESSAGE})


def bling_signup(request):
    if request.method == 'GET':
        return render(request, 'registration/signup.html')
    elif request.method == 'POST':
        ERROR_MESSAGE = 'Проверьте правильность введенных данных'
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # email = request.POST.get('email')
        if password == password2:
            try:
                User.objects.get(username=username)
                ERROR_MESSAGE = 'Имя ' + username + ' уже занято'
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, password=password)
                return redirect('/')
        return render(request, 'registration/signup.html', context={'error_message': ERROR_MESSAGE})


def bling_logout(request):
    logout(request)
    return redirect('/')


@login_required()
def index(request):
    if request.method == 'POST':
        scan_for_forms(request)
        return HttpResponseRedirect('/')
    blingposts = BlingPost.objects.all()
    context = {'blingposts': blingposts}
    return render(request, 'bling/index.html', context)


@login_required()
def user_profile(request, user_id):
    if request.method == 'POST':
        scan_for_forms(request)
        return HttpResponseRedirect(reverse('user_profile', args=[user_id]))
    blinguser = User.objects.get(username=user_id)
    # get friends list and amount
    friends = blinguser.profile.friends.all()
    friends_amount = len(friends)
    # get subs list and amount
    subs = blinguser.profile.subscribers.all()
    subs_amount = len(subs)
    # get all user's posts
    blingposts = BlingPost.objects.filter(author=blinguser)

    # check if request user is subscribed/friended to this user to decide which button to render
    if request.user in subs:
        is_current_user_subscribed = True
        is_current_user_friend = False
    elif request.user in friends:
        is_current_user_subscribed = False
        is_current_user_friend = True
    else:
        is_current_user_subscribed = False
        is_current_user_friend = False

    # check if friends and subs are more than 3, then they won't fit on the user page
    if friends_amount > 3:
        friends = friends[:3]
    if subs_amount > 3:
        subs = subs[:3]

    # check last online of profile

    # UPD: "current user" means request.user
    context = {
        'blinguser': blinguser,
        'blingposts': blingposts,
        'friends': friends,
        'friends_amount': friends_amount,
        'subs': subs,
        'subs_amount': subs_amount,
        'is_current_user_subscribed': is_current_user_subscribed,
        'is_current_user_friend': is_current_user_friend,
    }
    return render(request, 'bling/user_profile.html', context)


@login_required()
def notifications(request):
    notifications_list = []
    for n in BlingNotification.objects.all():
        if n.target_user == request.user:
            if (datetime.datetime.now().timestamp() - n.created_on.timestamp()) > 604800.0:
                n.delete()
            else:
                notifications_list.append(deepcopy(n))
                n.is_seen = True
                n.save()
    request.user.profile.notifications_amount = 0
    request.user.profile.save()
    context = {
        'notifications_list': notifications_list,
    }
    return render(request, 'bling/notifications.html', context)
