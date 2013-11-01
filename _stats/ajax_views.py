#!/usr/bin/python
# -*- coding: utf-8 -*-
from stats.models import *
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.encoding import smart_str , force_text

def getTeamList(request):
    season_id = request.GET.get('season_id',request.POST.get('season_id',None))
    tList = Team.objects.filter(season=season_id)
    
    resList = []
    
    for t in tList:
        cur = {}
        for a in t._meta.fields:
            ss = t.serializable_value(a.name)
            cur[a.name] = ss

        resList.append(cur)
    
    json_return = simplejson.dumps({'result':resList})
    return HttpResponse(json_return)

def getPlayerList(request):
    team_id = request.GET.get('team_id',request.POST.get('team_id',None))
    pList = Player.objects.filter(team=team_id)
    
    resList = []
    for p in pList:
        cur = {}
        for a in p._meta.fields:
            ss = p.serializable_value(a.name)
            cur[a.name] = ss

        resList.append(cur)
    
    json_return = simplejson.dumps({'result':resList})
    return HttpResponse(json_return)