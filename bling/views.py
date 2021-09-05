from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import BlingUser


def index(request):
    template = loader.get_template('bling/index.html')
    blingusers = BlingUser.objects.all()
    context = {'blingusers': blingusers}
    return HttpResponse(template.render(context, request))

