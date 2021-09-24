from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from .models import BlingPost, UserProfile
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import BlingPostForm


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


# class BlingPostDeleteView(LoginRequiredMixin, DeleteView):
#     model = BlingPost
#     success_url = '/'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         return context

def index(request):
    blingposts = BlingPost.objects.all()
    context = {'blingposts': blingposts}
    return render(request, 'bling/index.html', context)


def user_profile(request, user_id):
    blinguser = User.objects.get(username=user_id)  # basic user fields
    try:
        # custom user fields (born_on, friends, etc.)
        custom_user_fields = UserProfile.objects.get(user=User.objects.get(username=user_id))
        # get friends list and amount
        friends = custom_user_fields.friends.all()
        friends_amount = len(friends)
        # get subs list and amount
        subs = custom_user_fields.subscribers.all()
        subs_amount = len(subs)
    except UserProfile.DoesNotExist:
        friends = []
        subs = []
        friends_amount = 0
        subs_amount = 0
        custom_user_fields = None

    blingposts = BlingPost.objects.filter(author=blinguser)  # posts of this user

    # check if it is request.user's page or not so they cannot self-(un)subscribe
    if request.user == blinguser:
        # this page is request.user's own, must do nothing
        is_own_page = True
        is_current_user_subscribed = None
    else:
        # it's someone else's page, user can (un)subscribe
        is_own_page = False
        # check if current user is subscribed to this user to decide which button to render
        if request.user in subs:
            is_current_user_subscribed = True
        else:
            is_current_user_subscribed = False

    # check if friends and subs are more than 3, then they won't fit on the user page
    if friends_amount > 3:
        friends = friends[:3]
    if subs_amount > 3:
        subs = subs[:3]

    context = {
        'blinguser': blinguser,
        'blingposts': blingposts,
        'custom_user_fields': custom_user_fields,
        'friends': friends,
        'friends_amount': friends_amount,
        'subs': subs,
        'subs_amount': subs_amount,
        'is_own_page': is_own_page,
        'is_current_user_subscribed': is_current_user_subscribed,
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
        subscribant_user = User.objects.get(username=subscribant_username)
        subscribant_userprofile = UserProfile.objects.get(user=subscribant_user)
        subscribant_userprofile.subscribers.add(request.user)
        new_url = '/user/' + subscribant_username + '/'
        return redirect(new_url)
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")


def unsubscribe(request, subscribant_username):
    try:
        subscribant = User.objects.get(username=subscribant_username)
        # custom subscribant-user fields (born_on, friends, etc.)
        custom_subscribant = UserProfile.objects.get(user=User.objects.get(username=subscribant_username))
        custom_subscribant.subscribers.remove(request.user)
        new_url = '/user/' + subscribant_username + '/'
        return redirect(new_url)
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")
