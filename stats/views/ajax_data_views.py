#!/usr/bin/python
# -*- coding: utf-8 -*-
from stats.models import *
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.encoding import smart_str , force_text

from django.views.decorators.csrf import csrf_exempt

from django.forms import ValidationError

@csrf_exempt
def saveMatchPlayer(request):
    mp_id     = getReq(request , 'match_player_id')
    match_id  = getReq(request , 'match_id')
    team_id   = getReq(request , 'team_id')
    player_id = getReq(request , 'player')
    cs        = getReq(request , 'cs')
    gold      = getReq(request , 'gold')
    kill      = getReq(request , 'kill')
    death     = getReq(request , 'death')
    assist    = getReq(request , 'assist')
    mvp_point = getReq(request , 'mvp_point')
    pos       = getReq(request , 'pos')
    
    try:
        match = Match.objects.get(pk=match_id)
        team  = Team.objects.get(pk=team_id)
        player= Player.objects.get(pk=player_id)

        (mpSave , created) = Match_player.objects.get_or_create( season = match.season, team   = team, player = player, match  = match)
        mpSave.cs        = cs
        mpSave.gold      = gold
        mpSave.kill      = kill
        mpSave.death     = death
        mpSave.assist    = assist
        mpSave.mvp_point = mvp_point
        
        mpSave.save()

        p = 0
        if pos.lower().find('blue') >= 0:
            if pos.lower().find('top') >= 0:
                p=1
                match.bt = mpSave
            elif pos.lower().find('jungle') >= 0:
                p=2
                match.bj = mpSave
            elif pos.lower().find('mid') >= 0:
                p=3
                match.bm = mpSave
            elif pos.lower().find('ad') >= 0:
                p=4
                match.ba = mpSave
            elif pos.lower().find('support') >= 0:
                p=5
                match.bs = mpSave
        elif pos.lower().find('purple') >= 0:
            if pos.lower().find('top') >= 0:
                p=6
                match.pt = mpSave
            elif pos.lower().find('jungle') >= 0:
                p=7
                match.pj = mpSave
            elif pos.lower().find('mid') >= 0:
                p=8
                match.pm = mpSave
            elif pos.lower().find('ad') >= 0:
                p=9
                match.pa = mpSave
            elif pos.lower().find('support') >= 0:
                p=10
                match.ps = mpSave
        print '---'
        print pos.lower()
        print p
        print '---'
        match.save()

        json_return = simplejson.dumps({'result':'success'})
    except Exception , e:
        print e
        json_return = simplejson.dumps({'result':'fail'})
    
    return HttpResponse(json_return)

@csrf_exempt
def saveMatchResult(request):
    match_id = getReq(request , 'match_id')
    
    winner = getReq(request , 'winner')
    play_time = getReq(request , 'play_time')
    mvp = getReq(request , 'mvp')
    
    blue_ban1 = getReq(request , 'blue_ban1')
    blue_ban2 = getReq(request , 'blue_ban2')
    blue_ban3 = getReq(request , 'blue_ban3')
    
    purple_ban1 = getReq(request , 'purple_ban1')
    purple_ban2 = getReq(request , 'purple_ban2')
    purple_ban3 = getReq(request , 'purple_ban3')

    try:
        if not match_id and not winner:
            raise ValidationError('no params')
        
        match = Match.objects.get(pk=match_id)
        
        match.winner      = Team.objects.get(pk=winner)
        match.play_time   = play_time
        match.mvp         = Player.objects.get(pk=mvp)
        match.blue_ban1   = Champ.objects.get(pk=blue_ban1)
        match.blue_ban2   = Champ.objects.get(pk=blue_ban2)
        match.blue_ban3   = Champ.objects.get(pk=blue_ban3)
        match.purple_ban1 = Champ.objects.get(pk=purple_ban1)
        match.purple_ban2 = Champ.objects.get(pk=purple_ban2)
        match.purple_ban3 = Champ.objects.get(pk=purple_ban3)
        
        match.save()
        
        
        json_return = simplejson.dumps({'result':'success'})
    except Exception , e:
        print e
        json_return = simplejson.dumps({'result':'fail'})
    
    print json_return
    return HttpResponse(json_return)
            
@csrf_exempt    
def getTeamList(request):
    season_id = request.GET.get('season_id',request.POST.get('season_id',None))
    match_id = request.GET.get('match_id',request.POST.get('match_id',None))
    
    tList = []
    if season_id :
        tList = Team.objects.filter(season=season_id)
    if match_id :
        mList  = Match.objects.filter(pk=match_id)
        if len(mList) > 0:
            m = mList[0]
            tList.append( m.blue_team )
            tList.append( m.purple_team )
            
    
    resList = []
    
    for t in tList:
        cur = {'display': smart_str(t.__unicode__())}
        for a in t._meta.fields:
            ss = t.serializable_value(a.name)
            cur[a.name] = ss

        resList.append(cur)
    
    json_return = simplejson.dumps({'result':resList})
    return HttpResponse(json_return)

@csrf_exempt
def getPlayerList(request):
    team_id = request.GET.get('team_id',request.POST.get('team_id',None))
    pList = Player.objects.filter(team=team_id)
    
    resList = []
    resList = dbTOjson(pList)
    
    json_return = simplejson.dumps({'result':resList})
    return HttpResponse(json_return)

@csrf_exempt
def getMatchList(request):
    season_id = request.GET.get('season_id',request.POST.get('season_id',None))
    mList = Match.objects.filter(season=season_id).order_by('-match_id')
    
    resList = []
    for m in mList:
        cur = {'display': smart_str(m.__unicode__())}
        for a in m._meta.fields:
            ss = m.serializable_value(a.name)
            if ss == None:
                ss = ''
            cur[a.name] = smart_str(ss)
        resList.append(cur)

    json_return = simplejson.dumps({'result':resList})
    return HttpResponse(json_return)

@csrf_exempt
def getMatchPlayerList(request):
    match_id = request.GET.get('match_id',request.POST.get('match_id',None))
    team_id  = request.GET.get('team_id',request.POST.get('team_id',None))
    
    mpList = Match_player.objects.filter( match=match_id , team=team_id )
    
    resList = []
    if len(mpList) > 0 :
        resList = dbTOjson( mpList )

    json_return = simplejson.dumps({'result':resList})
    return HttpResponse(json_return)


def dbTOjson( list ):
    resList = []
    for o in list:
        if o.__unicode__:
            cur = {'display' : smart_str(o.__unicode__())}
        for a in o._meta.fields:
            cur[a.name] = smart_str( o.serializable_value(a.name) )
        
        resList.append(cur)
    
    return resList

def getReq( request , paramStr ):
    return request.GET.get(paramStr,request.POST.get(paramStr,None))