# This code will parse the play by play SportVU XML files and output a CSV file

import xml.etree.ElementTree as etree
import csv

# parse the entire file
tree = etree.parse('D:\Basketball\pistons\sportsvu\NBA_FINALPBP_EXP$2016060209.XML')

# open a csv file for writing
pbp_data = open('pbp.csv', 'wb')

# create a csv writer object and write the headers
csvwriter = csv.writer(pbp_data)
pbp_headers = ['league', 
               'league_id', 
               'season', 
               'gamecode', 
               'game_id', 
               'gametype_id', 
               'gametype', 
               'gamedate', 
               'gametime', 
               'away_team',
               'away_team_id',
               'away_team_score',
               'away_team_q1_score',
               'away_team_q1_fouls',
               'away_team_q2_score',
               'away_team_q2_fouls',
               'away_team_q3_score',
               'away_team_q3_fouls',
               'away_team_q4_score',
               'away_team_q4_fouls',
               'away_team_outcome',
               'home_team', 
               'home_team_id',
               'home_team_score',
               'home_team_q1_score',
               'home_team_q1_fouls',
               'home_team_q2_score',
               'home_team_q2_fouls',
               'home_team_q3_score',
               'home_team_q3_fouls',
               'home_team_q4_score',
               'home_team_q4_fouls',
               'home_team_outcome',
               'stadium',
               'quarter',
               'oncourt_id',
               'time_minutes',
               'time_seconds',
               'pbp_id',
               'global_player_id_1',
               'player_id_1',
               'display_name_1',
               'team_code_1',
               'team_alias_1',
               'global_player_id_2',
               'player_id_2',
               'display_name_2',
               'team_code_2',
               'team_alias_2',
               'global_player_id_3',
               'player_id_3',
               'display_name_3',
               'team_code_3',
               'team_alias_3',
               'points_type',
               'event_id',
               'event_description',
               'detail_id',
               'detail_description',
               'blocked',
               'distance',
               'x_shot_coord',
               'y_shot_coord',
               'fastbreak',
               'in_paint',
               'second_chance',
               'off_turnover',
               'player_score',
               'player_fouls',
               'visitor_score',
               'home_score',
               'visitor_fouls',
               'home_fouls',
               'position_id',
               'position',
               'textual_description'
               ]
                   
csvwriter.writerow(pbp_headers)

# before we traverse through the data, read in the common values needed for all rows                   
commonrows = []

for node in tree.iter('league'):
    commonrows.append(node.attrib.get('alias'))
    commonrows.append(node.attrib.get('global-id'))
for node in tree.iter('season'):
    commonrows.append(node.attrib.get('season'))
for node in tree.iter('gamecode'):
    commonrows.append(node.attrib.get('code'))
    commonrows.append(node.attrib.get('global-id'))
for node in tree.iter('gametype'):
    commonrows.append(node.attrib.get('id'))
    commonrows.append(node.attrib.get('type'))
for node in tree.iter('nba-playbyplay'):
    for child in node:
        if child.tag == 'date':
            commonrows.append(child.attrib.get('year') + '-' + child.attrib.get('month').zfill(2) + '-' + child.attrib.get('date').zfill(2))
for node in tree.iter('local-time'):
    commonrows.append(node.attrib.get('hour') + ':' + node.attrib.get('minute'))
for node in tree.iter('visiting-team'):
    for child in node:
        if child.tag == 'team-name':
            commonrows.append(child.attrib.get('alias'))
        if child.tag =='team-code':
            commonrows.append(child.attrib.get('id'))
        if child.tag =='linescore':
            commonrows.append(child.attrib.get('score'))
            for quarter in child:
                # could probably just loop through and do these sequentially,
                # but safer to be explicit in case they're not in order
                if quarter.attrib.get('quarter') == '1':
                    commonrows.append(quarter.attrib.get('score'))
                    commonrows.append(quarter.attrib.get('team-fouls'))
                if quarter.attrib.get('quarter') == '2':
                    commonrows.append(quarter.attrib.get('score'))
                    commonrows.append(quarter.attrib.get('team-fouls'))
                if quarter.attrib.get('quarter') == '3':
                    commonrows.append(quarter.attrib.get('score'))
                    commonrows.append(quarter.attrib.get('team-fouls'))
                if quarter.attrib.get('quarter') == '4':
                    commonrows.append(quarter.attrib.get('score'))
                    commonrows.append(quarter.attrib.get('team-fouls'))
for node in tree.iter('outcome-visit'):
    commonrows.append(node.attrib.get('outcome'))
        
for node in tree.iter('home-team'):
    for child in node:
        if child.tag == 'team-name':
            commonrows.append(child.attrib.get('alias'))
        if child.tag =='team-code':
            commonrows.append(child.attrib.get('id'))
        if child.tag =='linescore':
            commonrows.append(child.attrib.get('score'))
            for quarter in child:
                # could probably just loop through and do these sequentially,
                # but safer to be explicit in case they're not in order
                if quarter.attrib.get('quarter') == '1':
                    commonrows.append(quarter.attrib.get('score'))
                    commonrows.append(quarter.attrib.get('team-fouls'))
                if quarter.attrib.get('quarter') == '2':
                    commonrows.append(quarter.attrib.get('score'))
                    commonrows.append(quarter.attrib.get('team-fouls'))
                if quarter.attrib.get('quarter') == '3':
                    commonrows.append(quarter.attrib.get('score'))
                    commonrows.append(quarter.attrib.get('team-fouls'))
                if quarter.attrib.get('quarter') == '4':
                    commonrows.append(quarter.attrib.get('score'))
                    commonrows.append(quarter.attrib.get('team-fouls'))
for node in tree.iter('outcome-home'):
    commonrows.append(node.attrib.get('outcome'))

for node in tree.iter('stadium'):
    commonrows.append(node.attrib.get('name'))
    
# we have a list of all of the rows that will be the same
# now we need to traverse through and get all of the pbp data

pbp = []
for node in tree.iter('play'):
    pbp.append(node.attrib.get('quarter'))
    pbp.append(node.attrib.get('oncourt-id'))
    pbp.append(node.attrib.get('time-minutes'))
    pbp.append(node.attrib.get('time-seconds'))
    pbp.append(node.attrib.get('id'))
    pbp.append(node.attrib.get('global-player-id-1'))
    pbp.append(node.attrib.get('player-id-1'))
    pbp.append(node.attrib.get('display-name-1'))
    pbp.append(node.attrib.get('team-code-1'))
    pbp.append(node.attrib.get('team-alias-1'))
    pbp.append(node.attrib.get('global-player-id-2'))
    pbp.append(node.attrib.get('player-id-2'))
    pbp.append(node.attrib.get('display-name-2'))
    pbp.append(node.attrib.get('team-code-2'))
    pbp.append(node.attrib.get('team-alias-2'))
    pbp.append(node.attrib.get('global-player-id-3'))
    pbp.append(node.attrib.get('player-id-3'))
    pbp.append(node.attrib.get('display-name-3'))
    pbp.append(node.attrib.get('team-code-3'))
    pbp.append(node.attrib.get('team-alias-3'))
    pbp.append(node.attrib.get('points-type'))
    pbp.append(node.attrib.get('event_id'))
    pbp.append(node.attrib.get('event-description'))
    pbp.append(node.attrib.get('detail-id'))
    pbp.append(node.attrib.get('detail-description'))
    pbp.append(node.attrib.get('blocked'))
    pbp.append(node.attrib.get('distance'))
    pbp.append(node.attrib.get('x-shot-coord'))
    pbp.append(node.attrib.get('y-shot-coord'))
    pbp.append(node.attrib.get('fastbreak'))
    pbp.append(node.attrib.get('in-paint'))
    pbp.append(node.attrib.get('second-chance'))
    pbp.append(node.attrib.get('off-turnover'))
    pbp.append(node.attrib.get('player-score'))
    pbp.append(node.attrib.get('player-fouls'))
    pbp.append(node.attrib.get('visitor-score'))
    pbp.append(node.attrib.get('home-score'))
    pbp.append(node.attrib.get('visitor-fouls'))
    pbp.append(node.attrib.get('home-fouls'))
    pbp.append(node.attrib.get('position-id'))
    pbp.append(node.attrib.get('position'))
    pbp.append(node.attrib.get('textual-description'))
    csvwriter.writerow(commonrows + pbp)
    pbp = []

pbp_data.close()