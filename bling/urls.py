from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from .views import index, user_profile, BlingPostCreateView, remove_post, subscribe, unsubscribe
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user/<str:user_id>/', user_profile, name='user_profile'),
    path('newpost/', BlingPostCreateView.as_view(), name='newpost'),
    # path('newpost/', newpost, name='newpost'),
    path('removepost/<int:post_id>/', remove_post, name='remove_post'),
    path('subscribe/<str:subscribant_username>/', subscribe, name='subscribe'),
    path('unsubscribe/<str:subscribant_username>/', unsubscribe, name='unsubscribe'),
    path('', index, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)