#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from info.models import Player
from info.models import Team
from info.models import Season
# Create your models here.

class MatchPlayer(models.Model):
    match_player_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player , null=True , related_name="+")
    champ = models.CharField(max_length=30)
    cs = models.PositiveSmallIntegerField()
    gold = models.PositiveSmallIntegerField()
    kill = models.PositiveSmallIntegerField()
    death = models.PositiveSmallIntegerField()
    assist = models.PositiveSmallIntegerField()

class MatchResult(models.Model):
    match_result_id    = models.AutoField(primary_key=True)
    match              = models.ForeignKey('Match')
    

class Match(models.Model):
    match_id       = models.AutoField(primary_key=True)
    match_date     = models.DateField(null=True)
    match_time     = models.TimeField(null=True)
    
    season         = models.ForeignKey(Season)

    blue_team      = models.ForeignKey(Team   ,null=True , related_name="+")
    purple_team    = models.ForeignKey(Team   ,null=True , related_name="+")
    
    blue_top       = models.ForeignKey(Player ,blank=True , null=True , default=0 , related_name="+")
    blue_jungle    = models.ForeignKey(Player ,blank=True , null=True , default=0 , related_name="+")
    blue_mid       = models.ForeignKey(Player ,blank=True , null=True , default=0 , related_name="+")
    blue_ad        = models.ForeignKey(Player ,blank=True , null=True , default=0 , related_name="+")
    blue_support   = models.ForeignKey(Player ,blank=True , null=True , default=0 , related_name="+")
    
    purple_top     = models.ForeignKey(Player ,blank=True , null=True , default=0 , related_name="+")
    purple_jungle  = models.ForeignKey(Player ,blank=True , null=True , default=0 , related_name="+")
    purple_mid     = models.ForeignKey(Player ,blank=True , null=True , default=0 , related_name="+")
    purple_ad      = models.ForeignKey(Player ,blank=True , null=True , default=0 , related_name="+")
    purple_support = models.ForeignKey(Player ,blank=True , null=True , default=0 , related_name="+")
    
    def __unicode__(self):
        return 'Match No ' + str(self.match_id) + ': '+self.blue_team.name + ' vs ' + self.purple_team.name + ' at ' + str(self.match_date) + ' '+ str(self.match_time)[0:5]
    
    def save(self):
        print 'keke'
        pass
        
    class Meta:
        app_label = 'stats'
