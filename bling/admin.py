from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


@admin.register(BlingPost)
class BlingPostAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_on')
    list_display_links = ('author', )
    search_fields = ('author', 'created_on')


@admin.register(BlingImage)
class BlingImageAdmin(admin.ModelAdmin):
    list_display = ('created_on', 'owner')
    list_display_links = ('created_on', 'owner')
    search_fields = ('created_on', 'owner')


@admin.register(BlingComment)
class BlingCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_on')
    list_display_links = ('author', 'created_on')
    search_fields = ('author', 'created_on')


class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'


# определяем новый класс настроек для модели User
class UserAdmin(UserAdmin):
    inlines = (UserInline, )


# перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
