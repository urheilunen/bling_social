from django.forms import ModelForm

from .models import BlingPost


class BlingPostForm(ModelForm):
    class Meta:
        model = BlingPost
        exclude = ['author',]
