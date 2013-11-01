from django.contrib import admin
from info.models import Player
from info.models import Team
from info.models import Season
from info.models import Champ

class TeamPlayerInline(admin.TabularInline):
    model = Player

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name' , 'season')
    inlines = [TeamPlayerInline]

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name' , 'team' , 'prefer_position1', 'prefer_position2', 'prefer_position3' , 'current_teer')

admin.site.register(Player , PlayerAdmin)
admin.site.register(Season)
admin.site.register(Champ)
admin.site.register(Team , TeamAdmin)