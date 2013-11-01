from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    #page view                       
    url(r'match/result/insertForm/$' , 'stats.views.match_views.resultInsertForm' , name='match_result_insert_form'),
        #ajax inc page view
        url(r'match/result/insertForm/matchResult/$' , 'stats.views.ajax_views.matchResultForm'  , name='match_result_matchresult_form'),
    
    #page view - result
    url(r'result/standing/$' , 'stats.views.result_views.standing' , name='result_standing'),
    url(r'result/personal/$' , 'stats.views.result_views.personal' , name='result_personal'),
    
    #ajax getData
    url(r'^ajax/getTeamList/$', 'stats.views.ajax_data_views.getTeamList' , name='ajax_stat_get_team_list'),
    url(r'^ajax/getPlayerList/$', 'stats.views.ajax_data_views.getPlayerList' , name='ajax_stat_get_player_list'), 
    url(r'^ajax/getMatchList/$', 'stats.views.ajax_data_views.getMatchList' , name='ajax_stat_get_match_list'),
    url(r'^ajax/getMatchPlayerList/$', 'stats.views.ajax_data_views.getMatchPlayerList' , name='ajax_stat_get_matchplayer_list'),
    
    #ajax setDate
    url(r'^ajax/setMatchResult/$', 'stats.views.ajax_data_views.saveMatchResult' , name='ajax_stat_set_match_result'),
    url(r'^ajax/setMatchPlayer/$', 'stats.views.ajax_data_views.saveMatchPlayer' , name='ajax_stat_set_match_player'),
)