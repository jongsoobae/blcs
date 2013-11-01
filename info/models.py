#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

OBJ_POSITION = (
    ('N' , 'None'),
    ('T' , 'Top'),
    ('J' , 'Jungle'),
    ('M' , 'Mid'),
    ('A' , 'Ad'),
    ('S' , 'Support'),
)

OBJ_TEER = (
    ('N' , 'None'),
    ('01' , 'Bronze 5'),    ('02' , 'Bronze 4'),    ('03' , 'Bronze 3'),    ('04' , 'Bronze 2'),    ('05' , 'Bronze 1'),
    ('07' , 'Silver 5'),    ('08' , 'Silver 4'),    ('09' , 'Silver 3'),    ('10' , 'Silver 2'),    ('11' , 'Silver 1'),
    ('13' , 'Gold 5'),    ('14' , 'Gold 4'),    ('15' , 'Gold 3'),    ('16' , 'Gold 2'),    ('17' , 'Gold 1'),
    ('19' , 'Platinum 5'),    ('20' , 'Platinum 4'),    ('21' , 'Platinum 3'),    ('22' , 'Platinum 2'),    ('23' , 'Platinum 1'),
    ('25' , 'Diamond 5'),    ('26' , 'Diamond 4'),    ('27' , 'Diamond 3'),    ('28' , 'Diamond 2'),    ('29' , 'Diamond 1'),
    ('35' , 'Challenger'),
)

OBJ_LEADER = ( ('yes' , 'Leader') , ('no' , 'Player') )

OBJ_PLAYING = ( ('yes' , 'Current Playing') , ('no' , 'Not Player') )

class Season(models.Model):
    season_id = models.AutoField(primary_key=True)
    season_no = models.PositiveSmallIntegerField()
    
    def __unicode__(self):
        return 'Season ' + str(self.season_no)

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    season = models.ForeignKey(Season)
    
    def __unicode__(self):
        return self.name
    
class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    team = models.ForeignKey(Team , null=True)
    prefer_position1 = models.CharField(max_length=1,choices=OBJ_POSITION , null=True , default='N')
    prefer_position2 = models.CharField(max_length=1,choices=OBJ_POSITION , null=True , default='N')
    prefer_position3 = models.CharField(max_length=1,choices=OBJ_POSITION , null=True , default='N')
    prefer_position4 = models.CharField(max_length=1,choices=OBJ_POSITION , null=True , default='N')
    prefer_position5 = models.CharField(max_length=1,choices=OBJ_POSITION , null=True , default='N')
    current_teer = models.CharField(max_length=2,choices=OBJ_TEER , null=True)
    b_leader = models.CharField(max_length=3, choices=OBJ_LEADER , null=True , default='no')
    b_playing = models.CharField(max_length=3,choices=OBJ_PLAYING , null=True , default='yes')

    def __unicode__(self):
        return self.name

class Champ(models.Model):
    champ_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name