from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from .views import index, user_profile, BlingPostCreateView, newpost

urlpatterns = [
    path('user/<str:user_id>/', user_profile, name='user_profile'),
    # path('newpost/', BlingPostCreateView.as_view(), name='newpost'),
    path('newpost/', newpost, name='newpost'),
    path('', index, name='home'),
]