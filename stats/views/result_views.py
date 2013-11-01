#!/usr/bin/python
# -*- coding: utf-8 -*-
from stats.models import *
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.encoding import smart_str , force_text

from django.shortcuts import render

def personal(request):
    order_field = getReq(request , 'order_field')
    order_by = getReq(request , 'order_by')
    season_id = getReq(request , 'season_id')
    if not season_id:
        season_id = 0
    
    players    = Player.objects.filter( team__season=season_id )
    matches = Match.objects.filter( season=season_id , match_type = 'R' )
    result = {}
    personal_result = []
    
    try :
        for player in players:
            player.pick = 0
            player.kill = 0
            player.death = 0
            player.assist = 0
            player.cs = 0
            player.gold = 0
            player.play_time = 0
            player.teamkill = 0
            
            player.kda = 0.0
            player.killof = 0.0
            player.csm = 0.0
            player.goldm = 0.0
            
            player.mvp = 0
            
            result[player.pk]=player
        
        for _match in matches:
            mbps = [ _match.bt , _match.bj , _match.bm , _match.ba , _match.bs , _match.pt , _match.pj , _match.pm , _match.pa , _match.ps ]
            
            for mbp in mbps:
                if mbp:
                    result[mbp.player.pk].pick       += 1
                    result[mbp.player.pk].kill       += mbp.kill
                    result[mbp.player.pk].death      += mbp.death
                    result[mbp.player.pk].assist     += mbp.assist
                    result[mbp.player.pk].cs         += mbp.cs
                    result[mbp.player.pk].gold       += mbp.gold
                    result[mbp.player.pk].mvp        += mbp.mvp_point
                    result[mbp.player.pk].play_time  += _match.play_time
                    
                    if mbp.player.team.pk == _match.blue_team.pk:
                        for _mbp in mbps[0:5]:
                            result[mbp.player.pk].teamkill   += _mbp.kill
                        #result[mbp.player.pk].teamkill   += (_match.bt.kill + _match.bj.kill + _match.bm.kill + _match.ba.kill + _match.bs.kill)
                    else:
                        for _mbp in mbps[5:10]:
                            result[mbp.player.pk].teamkill   += _mbp.kill
                        #result[mbp.player.pk].teamkill   += (_match.pt.kill + _match.pj.kill + _match.pm.kill + _match.pa.kill + _match.ps.kill)
                
        for res in result:
            
            result[res].kda    = float(result[res].kill + result[res].assist) / result[res].death if result[res].death != 0 else 0 
            result[res].csm    = float(result[res].cs)   / result[res].play_time if result[res].play_time != 0 else 0 
            result[res].goldm  = float(result[res].gold) / result[res].play_time if result[res].play_time != 0 else 0
            result[res].killof = float(result[res].kill + result[res].assist) / result[res].teamkill if result[res].teamkill != 0 else 0
            result[res].kda = round( result[res].kda , 2)
            result[res].csm = round( result[res].csm , 2 )
            result[res].goldm = round( result[res].goldm , 2 )
            result[res].killof = round( result[res].killof , 2 )*100
            personal_result.append( result[res] )
    except Exception , e:
        print e
    
    if order_field:
        exec 'personal_result.sort( key=lambda x:x.' + order_field + ')'
    else :
        personal_result.sort( key=lambda x:x.kda )
    if order_by and order_by == 'u' :
        pass
    else :
        personal_result.reverse()
    
    context = { 'personalList' : personal_result 
            , 'seasonList' : Season.objects.all().order_by('-pk') 
            , 'season_id'  : season_id
            , 'order_field' : order_field
            , 'order_by' : order_by
            }
    
    return render( request , 'result/personal.html' , context )

def standing(request):
    order_field = getReq(request , 'order_field')
    order_by = getReq(request , 'order_by')
    season_id = getReq(request , 'season_id')
    if not season_id:
        season_id = 0
    
    standing = {}
    standing_result = []
    teams   = Team.objects.filter(  season=season_id )
    matchsets = MatchSet.objects.all()
    try :
        for team in teams:
            team.rank_point = 0;   team.play_cnt = 0;
            team.wcnt = 0;        team.dcnt = 0;     team.lcnt = 0
            team.det_wcnt = 0;    team.det_dcnt = 0; team.det_lcnt = 0
            team.b_wcnt = 0; team.b_dcnt = 0;  team.b_lcnt = 0
            team.p_wcnt = 0
            team.p_dcnt = 0
            team.p_lcnt = 0
            team.set_wcnt = 0
            team.set_dcnt = 0
            team.kill = 0
            team.death = 0
            team.assist = 0
            team.kda = 0.0
            team.cs = 0
            team.gold = 0
            team.play_time = 0
            team.csm = 0.0
            team.goldm = 0.0
            standing[team.pk]=team
        
        cur_bteam = None
        cur_pteam = None
        
        for _matchset in matchsets:
            matches = Match.objects.filter( season=season_id , match_type = 'R' , matchset=_matchset )
            
            for _match in matches:
                print 'b'
                cur_bteam = _match.blue_team
                print 'c'
                cur_pteam = _match.purple_team
                print 'd'
                
                nmp = Match_player()
                nmp.kill = 0; nmp.death = 0; nmp.assist = 0
                
                _match.bt = _match.bt if _match.bt else nmp
                _match.bj = _match.bj if _match.bj else nmp
                _match.bm = _match.bm if _match.bm else nmp
                _match.ba = _match.ba if _match.ba else nmp
                _match.bs = _match.bs if _match.bs else nmp
                _match.pt = _match.pt if _match.pt else nmp
                _match.pj = _match.pj if _match.pj else nmp
                _match.pm = _match.pm if _match.pm else nmp
                _match.pa = _match.pa if _match.pa else nmp
                _match.ps = _match.ps if _match.ps else nmp
                               
                standing[cur_bteam.pk].play_time += _match.play_time
                standing[cur_bteam.pk].gold   += ( _match.bt.gold  + _match.bj.gold + _match.bm.gold   + _match.ba.gold   + _match.bs.gold )
                standing[cur_bteam.pk].cs     += ( _match.bt.cs   + _match.bj.cs   + _match.bm.cs   + _match.ba.cs   + _match.bs.cs )
                standing[cur_bteam.pk].kill   += ( _match.bt.kill   + _match.bj.kill   + _match.bm.kill   + _match.ba.kill   + _match.bs.kill )
                standing[cur_bteam.pk].death  += ( _match.bt.death  + _match.bj.death  + _match.bm.death  + _match.ba.death  + _match.bs.death )
                standing[cur_bteam.pk].assist += ( _match.bt.assist + _match.bj.assist + _match.bm.assist + _match.ba.assist + _match.bs.assist )
                standing[cur_bteam.pk].kda     = float( standing[cur_bteam.pk].kill + standing[cur_bteam.pk].assist ) / standing[cur_bteam.pk].death if standing[cur_bteam.pk].death != 0 else standing[cur_bteam.pk].kill + standing[cur_bteam.pk].assist
                standing[cur_bteam.pk].goldm   = float(standing[cur_bteam.pk].gold) / standing[cur_bteam.pk].play_time if standing[cur_bteam.pk].play_time != 0 else 'NaN'
                standing[cur_bteam.pk].csm     = float(standing[cur_bteam.pk].cs)  / standing[cur_bteam.pk].play_time if standing[cur_bteam.pk].play_time != 0 else 'NaN'
                
                standing[cur_pteam.pk].play_time += _match.play_time
                standing[cur_pteam.pk].gold   += ( _match.pt.gold  + _match.pj.gold + _match.pm.gold   + _match.pa.gold   + _match.ps.gold )
                standing[cur_pteam.pk].cs     += ( _match.pt.cs   + _match.pj.cs   + _match.pm.cs   + _match.pa.cs   + _match.ps.cs )
                standing[cur_pteam.pk].kill   += ( _match.pt.kill + _match.pj.kill + _match.pm.kill + _match.pa.kill + _match.ps.kill )
                standing[cur_pteam.pk].death  += ( _match.pt.death + _match.pj.death + _match.pm.death + _match.pa.death + _match.ps.death )
                standing[cur_pteam.pk].assist += ( _match.pt.assist + _match.pj.assist + _match.pm.assist + _match.pa.assist + _match.ps.assist )
                standing[cur_pteam.pk].kda     = float( standing[cur_pteam.pk].kill + standing[cur_pteam.pk].assist ) / standing[cur_pteam.pk].death if standing[cur_pteam.pk].death != 0 else standing[cur_pteam.pk].kill + standing[cur_pteam.pk].assist
                standing[cur_pteam.pk].goldm   = float(standing[cur_pteam.pk].gold) / standing[cur_pteam.pk].play_time if standing[cur_pteam.pk].play_time != 0 else 'NaN'
                standing[cur_pteam.pk].csm     = float(standing[cur_pteam.pk].cs)  / standing[cur_pteam.pk].play_time if standing[cur_pteam.pk].play_time != 0 else 'NaN'
                
                if _match.winner == cur_bteam:
                    standing[cur_bteam.pk].set_wcnt += 1
                    standing[cur_bteam.pk].det_wcnt += 1; standing[cur_bteam.pk].b_wcnt += 1
                    standing[cur_pteam.pk].det_lcnt += 1; standing[cur_pteam.pk].p_dcnt += 1
                    
                elif _match.winner == _match.purple_team:
                    standing[cur_pteam.pk].set_wcnt += 1
                    standing[cur_bteam.pk].det_lcnt += 1; standing[cur_bteam.pk].b_lcnt += 1
                    standing[cur_pteam.pk].det_wcnt += 1; standing[cur_pteam.pk].p_wcnt += 1
            
            if standing[cur_bteam.pk].set_wcnt == 0 and standing[cur_pteam.pk].set_wcnt == 0:
                pass
            else :
                standing[cur_bteam.pk].play_cnt += 1; standing[cur_pteam.pk].play_cnt += 1
                if standing[cur_bteam.pk].set_wcnt > standing[cur_pteam.pk].set_wcnt:
                    standing[cur_bteam.pk].wcnt +=1; standing[cur_bteam.pk].rank_point += _match.matchset.wpoint
                    standing[cur_pteam.pk].lcnt +=1; standing[cur_pteam.pk].rank_point += _match.matchset.lpoint
                    
                elif standing[cur_pteam.pk].set_wcnt > standing[cur_bteam.pk].set_wcnt:
                    standing[cur_bteam.pk].lcnt +=1; standing[cur_bteam.pk].rank_point += _match.matchset.lpoint
                    standing[cur_pteam.pk].wcnt +=1; standing[cur_pteam.pk].rank_point += _match.matchset.wpoint
                
                elif standing[cur_bteam.pk].set_wcnt == standing[cur_pteam.pk].set_wcnt:
                    standing[cur_bteam.pk].dcnt +=1; standing[cur_bteam.pk].rank_point += _match.matchset.dpoint
                    standing[cur_pteam.pk].dcnt +=1; standing[cur_pteam.pk].rank_point += _match.matchset.dpoint
                
            standing[cur_bteam.pk].set_wcnt = 0; standing[cur_pteam.pk].set_wcnt = 0; 
            
        for st in standing:
            standing[st].kda    = float( standing[st].kill + standing[st].assist ) / standing[st].death if standing[st].death != 0 else standing[st].kill + standing[st].assist
            standing[st].goldm  = float(standing[st].gold) / standing[st].play_time if standing[st].play_time != 0 else 0 
            standing[st].csm    = float(standing[st].cs)  / standing[st].play_time if standing[st].play_time != 0 else 0
            standing[st].kda    = round( standing[st].kda , 2 )
            standing[st].goldm  = round( standing[st].goldm , 2 )
            standing[st].csm    = round( standing[st].csm , 2 )
            standing_result.append( standing[st] );
            print str(standing[st]) + "("+str(standing[st].rank_point)+") " +str(standing[st].wcnt)+"W "+str(standing[st].dcnt)+"D "+str(standing[st].lcnt)+"L[ "+str(standing[st].det_wcnt)+"W" + str(standing[st].det_lcnt) +"L]"
        
        if order_field:
            exec 'standing_result.sort( key=lambda x:x.' + order_field + ')'
        else :
            standing_result.sort( key=lambda x:x.rank_point )
        if order_by and order_by == 'u' :
            pass
        else :
            standing_result.reverse()
        #standing_result.sort( key=lambda x:x.rank_point )
        #standing_result.reverse()

    except Exception , e:
        print e
    
    context = { 'standing' : standing_result 
            , 'seasonList' : Season.objects.all().order_by('-pk') 
            , 'season_id'  : season_id
            , 'order_field' : order_field
            , 'order_by' : order_by
            }
    return render( request , 'result/standing.html' , context )

def getReq( request , paramStr ):
    return request.GET.get(paramStr,request.POST.get(paramStr,None))