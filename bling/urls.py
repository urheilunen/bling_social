from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user/<str:user_id>/', user_profile, name='user_profile'),
    path('notifications/', notifications, name='notifications'),
    path('signup/', bling_signup, name='signup'),  # register
    path('signin/', bling_signin, name='signin'),  # login
    path('logout', bling_logout, name='logout'),
    path('', index, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
