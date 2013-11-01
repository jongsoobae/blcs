from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^ajax/getTeamList/$', 'stats.ajax_views.getTeamList' , name='ajax_stat_get_team_list'),
    url(r'^ajax/getPlayerList/$', 'stats.ajax_views.getPlayerList' , name='ajax_stat_get_player_list'), 
)