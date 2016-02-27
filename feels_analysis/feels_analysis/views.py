from __future__ import absolute_import, print_function

from .models import *

from django.conf import settings
from django.http import HttpResponseServerError  # Http404
from django.shortcuts import render, get_object_or_404, redirect

def index(request):
    return render(request, 'index.html', {},)
