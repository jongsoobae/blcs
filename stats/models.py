#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from info.models import Champ
from info.models import Player
from info.models import Team
from info.models import Season

from django.utils.encoding import smart_str

# Create your models here.

OBJ_TYPE = (
 ('R', '정규시즌'),
 ('P', '플레이오프'),
)
class MatchSet(models.Model):
    description  = models.CharField(max_length=20 )
    wpoint       = models.PositiveSmallIntegerField(max_length=3, default=3 , null=True , blank=True)
    dpoint       = models.PositiveSmallIntegerField(max_length=3, default=1 , null=True , blank=True)
    lpoint       = models.PositiveSmallIntegerField(max_length=3, default=0 , null=True , blank=True)
    def __unicode__(self):
        return self.description
    
class Match(models.Model):
    match_id       = models.AutoField(primary_key=True)
    matchset       = models.ForeignKey('MatchSet')
    match_date     = models.DateField(null=True)
    match_time     = models.TimeField(null=True)
    match_type     = models.CharField(max_length=2,choices=OBJ_TYPE)
    
    season         = models.ForeignKey(Season)
    
    blue_team      = models.ForeignKey(Team   ,null=True , related_name="+")
    purple_team    = models.ForeignKey(Team   ,null=True , related_name="+")
    
    winner         = models.ForeignKey(Team   ,null=True , related_name="+")
    play_time      = models.FloatField(null=True , blank=True , default=0)
    
    blue_ban1      = models.ForeignKey(Champ , null=True , blank=True , related_name="+")
    blue_ban2      = models.ForeignKey(Champ , null=True , blank=True , related_name="+")
    blue_ban3      = models.ForeignKey(Champ , null=True , blank=True , related_name="+")
    
    purple_ban1    = models.ForeignKey(Champ , null=True , blank=True , related_name="+")
    purple_ban2    = models.ForeignKey(Champ , null=True , blank=True , related_name="+")
    purple_ban3    = models.ForeignKey(Champ , null=True , blank=True , related_name="+")
    
    mvp            = models.ForeignKey(Player , null=True , blank=True)
    
    bt       = models.ForeignKey('Match_player' , null=True , blank=True , related_name="+" )
    bj       = models.ForeignKey('Match_player' , null=True , blank=True , related_name="+" )
    bm       = models.ForeignKey('Match_player' , null=True , blank=True , related_name="+" )
    ba       = models.ForeignKey('Match_player' , null=True , blank=True , related_name="+" )
    bs       = models.ForeignKey('Match_player' , null=True , blank=True , related_name="+" )
    
    pt       = models.ForeignKey('Match_player' , null=True , blank=True , related_name="+" )
    pj       = models.ForeignKey('Match_player' , null=True , blank=True , related_name="+" )
    pm       = models.ForeignKey('Match_player' , null=True , blank=True , related_name="+" )
    pa       = models.ForeignKey('Match_player' , null=True , blank=True , related_name="+" )
    ps       = models.ForeignKey('Match_player' , null=True , blank=True , related_name="+" )
    
    def __unicode__(self):
        matches = Match.objects.filter(matchset = self.matchset , season = self.season).order_by('match_id')
        idx = 1
        for match in matches:
            if match.pk == self.match_id :
                break
            idx = idx + 1
        return self.matchset.description + ' ' + smart_str(idx) + u'경기'

class Match_player(models.Model):
    match_player_id = models.AutoField(primary_key=True)
    season          = models.ForeignKey(Season )
    team            = models.ForeignKey(Team   )
    player          = models.ForeignKey(Player )
    match           = models.ForeignKey(Match  )
    cs              = models.PositiveSmallIntegerField(max_length=5, default=0 , null=True , blank=True)
    gold            = models.PositiveSmallIntegerField(max_length=6, default=0 , null=True , blank=True)
    kill            = models.PositiveSmallIntegerField(max_length=3, default=0 , null=True , blank=True)
    death           = models.PositiveSmallIntegerField(max_length=3, default=0 , null=True , blank=True)
    assist          = models.PositiveSmallIntegerField(max_length=3, default=0 , null=True , blank=True)
    mvp_point       = models.PositiveSmallIntegerField(max_length=4, default=0 , null=True , blank=True)
    
    def __unicode__(self):
        return 'M'+str(self.match.match_id) + ': '+self.player.name
    
class Standing(models.Model):
    win_point = models.PositiveSmallIntegerField(max_length=3,default=0)
    team      = models.ForeignKey(Team   )
    
