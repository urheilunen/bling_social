from django.contrib import admin
from .models import *


class BlingUserAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'created_on', 'email')
    list_display_links = ('nickname', 'created_on', 'email')
    search_fields = ('nickname', 'created_on', 'email')


class BlingPostAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_on')
    list_display_links = ('author', )
    search_fields = ('author', 'created_on')


class BlingImageAdmin(admin.ModelAdmin):
    list_display = ('owner', 'created_on')
    list_display_links = ('owner', 'created_on')
    search_fields = ('owner', 'created_on')


class BlingCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_on')
    list_display_links = ('author', 'created_on')
    search_fields = ('author', 'created_on')


admin.site.register(BlingUser, BlingUserAdmin)
admin.site.register(BlingPost, BlingPostAdmin)
admin.site.register(BlingImage, BlingImageAdmin)
admin.site.register(BlingComment, BlingCommentAdmin)
