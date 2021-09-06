from django.forms import ModelForm

from .models import BlingUser, BlingPost


class BlingUserForm(ModelForm):
    class Meta:
        model = BlingUser
        fields = ('nickname', 'name', 'surname')


class BlingPostForm(ModelForm):
    class Meta:
        model = BlingPost
        # нужно будет убрать автора (сделать автодобавление на основе залогиненного юзера) и добавить поле изображения
        fields = ('text', 'author')
