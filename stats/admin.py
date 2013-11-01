#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from stats.models import Match , Match_player , MatchSet

class MatchPlayerInline(admin.TabularInline):
    model = Match_player
    fields           = ('team' , 'player' , 'cs' , 'gold' , 'kill' , 'death' , 'assist' , 'mvp_point')
    #field1 = (None , {'fields' : ['team' , 'player' , 'cs' , 'gold' , 'kill' , 'death' , 'assist' , 'mvp_point'] , 'classes' : ['collapse'] })
    #fieldsets = [ field1 ]
    readonly_fields = ( 'team' , 'player'  , 'cs' , 'gold' , 'kill' , 'death' , 'assist' , 'mvp_point')
    extra = 0
    
class MatchAdmin(admin.ModelAdmin):
    
    field1 = ('Match Info - 사전 입력' , {'fields':['match_date' , 'match_time' , 'season' , 'match_type', 'matchset', 'blue_team' , 'purple_team']})
    field2 = ('Result - readonly' , {'fields' : ['winner' , 'play_time' , 'blue_ban1' , 'blue_ban2' , 'blue_ban3' , 'purple_ban1' , 'purple_ban2' , 'purple_ban3' , 'mvp']})
    fieldsets = [
    field1 , field2
    ]
    inlines = [MatchPlayerInline]
    readonly_fields = ['winner' , 'play_time' , 'blue_ban1' , 'blue_ban2' , 'blue_ban3' , 'purple_ban1' , 'purple_ban2' , 'purple_ban3' , 'mvp']
    
admin.site.register(Match , MatchAdmin)
admin.site.register(Match_player)
admin.site.register(MatchSet)