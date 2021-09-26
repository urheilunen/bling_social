from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import BlingPost
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class BlingPostCreateView(LoginRequiredMixin, CreateView):
    model = BlingPost
    fields = ['text', 'images']
    template_name = 'bling/create_post.html'
    # form_class = BlingPostForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def index(request):
    blingposts = BlingPost.objects.all()
    context = {'blingposts': blingposts}
    return render(request, 'bling/index.html', context)


def user_profile(request, user_id):
    blinguser = User.objects.get(username=user_id)
    # get friends list and amount
    friends = blinguser.profile.friends.all()
    friends_amount = len(friends)
    # get subs list and amount
    subs = blinguser.profile.subscribers.all()
    subs_amount = len(subs)
    # get all user's posts
    blingposts = BlingPost.objects.filter(author=blinguser)

    # check if it is request.user's page or not so they cannot self-(un)subscribe
    if request.user == blinguser:
        # this page is request.user's own, must do nothing
        is_own_page = True
        is_current_user_subscribed = False
        is_current_user_friend = False
    else:
        # it's someone else's page, user can (un)subscribe
        is_own_page = False
        # check if current user is subscribed/friended to this user to decide which button to render
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

    context = {
        'blinguser': blinguser,
        'blingposts': blingposts,
        'friends': friends,
        'friends_amount': friends_amount,
        'subs': subs,
        'subs_amount': subs_amount,
        'is_own_page': is_own_page,
        'is_current_user_subscribed': is_current_user_subscribed,
        'is_current_user_friend': is_current_user_friend,
    }
    return render(request, 'bling/user_profile.html', context)


def remove_post(request, post_id):
    try:
        # searching for the post with this primary key
        post = BlingPost.objects.get(pk=int(post_id))
        # getting the author of the post to approve that the very author is deleting their creation
        post_author = post.author
        if request.user == post_author:
            # if deleting is requested by the author, then it's ok
            post.delete()
            # redirecting to the profile of author
            # because we are already there, user won't see the difference, post will just vanish in a moment
            new_url = '/user/' + post_author.username + '/'
            return redirect(new_url)
        else:
            # deleting is not requested by author. Go away, criminal scum
            return HttpResponseNotAllowed("<h2>Not allowed</h2>")
    except BlingPost.DoesNotExist:
        # no such post, wtf
        return HttpResponseNotFound("<h2>Post not found</h2>")


def subscribe(request, subscribant_username):
    try:
        new_url = '/user/' + subscribant_username + '/'  # firstly make a url to redirect to anytime function needs
        subscribant_user = User.objects.get(username=subscribant_username)  # get user to be sub-ed to by his username

        # get lists of sub-nt subs&friends for some checks
        subscribant_subs = subscribant_user.profile.subscribers.all()
        subscribant_friends = subscribant_user.profile.friends.all()

        # now check if request.user is already sub-ed (or friended)
        if request.user in subscribant_subs or request.user in subscribant_friends:
            # user is already sub-ed
            # go to sub-nt page without any alerts
            return redirect(new_url)

        # now check if sub-nt is sub-ed to request.user (if true, they must become friends :з)
        if subscribant_user in request.user.profile.subscribers.all():
            # yep, he is, remove it...
            request.user.profile.subscribers.remove(subscribant_user)
            # ...to make them friends
            subscribant_user.profile.friends.add(request.user)
            request.user.profile.friends.add(subscribant_user)
            return redirect(new_url)

        # not sub-ed, not friends, just a pure subscription
        subscribant_user.profile.subscribers.add(request.user)
        return redirect(new_url)
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")


def unsubscribe(request, subscribant_username):
    try:
        new_url = '/user/' + subscribant_username + '/' # firstly make an url to redirect to anytime function needs
        subscribant_user = User.objects.get(username=subscribant_username)  # get user to be unsub-ed by his username

        # get lists of sub-nt subs&friends for some checks
        subscribant_subs = subscribant_user.profile.subscribers.all()
        subscribant_friends = subscribant_user.profile.friends.all()

        # now check if request.user is unsub-ed
        if request.user not in subscribant_subs and request.user not in subscribant_friends:
            # user is already unsub-ed
            # go to sub-nt page without any alerts
            return redirect(new_url)

        # now check if sub-nt and request.user are friends
        if request.user in subscribant_friends:
            # yep, he is, unfriend them...
            subscribant_user.profile.friends.remove(request.user)
            request.user.profile.friends.remove(subscribant_user)
            # ...and just subscribe sub-nt to request.user
            request.user.profile.subscribers.add(subscribant_user)
            return redirect(new_url)

        # not friends, request.user is just sub-ed to sub-nt, just pure unsubscription
        subscribant_user.profile.subscribers.remove(request.user)
        return redirect(new_url)
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")
