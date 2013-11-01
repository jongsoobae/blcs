#!/usr/bin/python
# -*- coding: utf-8 -*-
from stats.models import *
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.encoding import smart_str , force_text

from django.shortcuts import render

def resultInsertForm(request):
    
    season_id = request.GET.get('season_id' , request.POST.get('season_id' , None ) )
    match_id = request.GET.get('match_id' , request.POST.get('match_id' , None ) )
    
    context = { 'seasonList' : Season.objects.all().order_by('-season_no')
               ,'matchList'  : Match.objects.filter(season = season_id)
               ,'match_id'   : match_id
               ,'season_id'  : season_id}
    
    return render( request , 'match/insert_form.html' , context )
