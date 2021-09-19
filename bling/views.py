from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import BlingPost, UserProfile
from django.contrib.auth.models import User
from .forms import BlingPostForm


class BlingPostCreateView(CreateView):
    template_name = 'bling/create_post.html'
    form_class = BlingPostForm
    success_url = '/'


def index(request):
    blingposts = BlingPost.objects.all()
    context = {'blingposts': blingposts}
    return render(request, 'bling/index.html', context)


def user_profile(request, user_id):
    blinguser = User.objects.get(username=user_id)
    blingposts = BlingPost.objects.filter(author=blinguser)
    context = {'blinguser': blinguser, 'blingposts': blingposts}
    return render(request, 'bling/user_profile.html', context)


def newpost(request):
    form = BlingPostForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('/')
    return render(request, 'bling/create_post.html')
