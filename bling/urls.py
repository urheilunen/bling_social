from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user/<str:user_id>/', user_profile, name='user_profile'),
    path('notifications/', notifications, name='notifications'),
    path('newpost/', BlingPostCreateView.as_view(), name='newpost'),
    path('removepost/<int:post_id>/', remove_post, name='remove_post'),
    path('subscribe/<str:subscribant_username>/', subscribe, name='subscribe'),
    path('unsubscribe/<str:subscribant_username>/', unsubscribe, name='unsubscribe'),
    path('signup/', bling_signup, name='signup'),  # register
    path('signin/', bling_signin, name='signin'),  # login
    path('logout', bling_logout, name='logout'),
    # path('like/<int:post_id>/', like_post, name='like_post'),
    # path('comment/<str:src_page>/<int:post_id>/', comment_post, name='comment_post'),
    path('', index, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
