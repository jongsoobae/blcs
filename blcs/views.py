#!/usr/bin/python
# -*- coding: utf-8 -*-
from stats.models import *
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.encoding import smart_str , force_text

from django.shortcuts import render

def index(request):
    
    context = {  }
    return render( request , 'index.html' , context )