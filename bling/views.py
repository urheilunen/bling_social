from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from .models import BlingPost, UserProfile
from django.contrib.auth.models import User
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
    }
    return render(request, 'bling/user_profile.html', context)
