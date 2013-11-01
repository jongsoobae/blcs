#!/usr/bin/python
# -*- coding: utf-8 -*-
from stats.models import *
from django.utils.encoding import smart_str

from django.shortcuts import render

def matchResultForm(request):
    match_id = request.GET.get('match_id',request.POST.get('match_id',None))
    
    match = None
    try :
        match = Match.objects.get(pk=match_id)
    except :
        pass
    
    b_players = Player.objects.filter(team = match.blue_team)
    p_players = Player.objects.filter(team = match.purple_team)
    
    champList = Champ.objects.all();
    
    match_player = Match_player.objects.filter(match=match).order_by('team')
    
    bmpObj = ( {'str':'Top'     , 'o' : match.bt , 'i' : 0}
              ,{'str':'Jungle'  , 'o' : match.bj , 'i' : 1}
              ,{'str':'Mid'     , 'o' : match.bm , 'i' : 2}
              ,{'str':'Ad'      , 'o' : match.ba , 'i' : 3}
              ,{'str':'Support' , 'o' : match.bs , 'i' : 4}
             )
    pmpObj = ( {'str':'Top'     , 'o' : match.pt , 'i' : 0}
              ,{'str':'Jungle'  , 'o' : match.pj , 'i' : 1}
              ,{'str':'Mid'     , 'o' : match.pm , 'i' : 2}
              ,{'str':'Ad'      , 'o' : match.pa , 'i' : 3}
              ,{'str':'Support' , 'o' : match.ps , 'i' : 4}
             )
    
    context = {  'match'        : match 
               , 'b_players'    : b_players 
               , 'p_players'    : p_players
               , 'champList'    : champList
               , 'match_player' : match_player
               , 'bmps'         : bmpObj
               , 'pmps'         : pmpObj
               , 'range5'       : range(0,5)
               , 'positons'     : ('Top' , 'Jungle' , 'Mid' , 'Ad' , 'Support')
               , 'mp_desc'      : ('포지션','플레이어','CS','GOLD','Kill','Death','Assist','Mvp Point')
               , 'mp_input_name': ('cs' , 'gold' , 'kill' , 'death' , 'assist' , 'mvp_point')
              }
    return render( request , 'match/inc_match_res.html' , context )
    