# This code will parse the play by play optical tracking SportVU XML files and output a CSV file

import xml.etree.ElementTree as etree
import csv

# parse the entire file
tree = etree.parse('D:\Basketball\pistons\sportsvu\NBA_FINAL_SEQUENCE_PBP_OPTICAL$2016060209.XML')

# open a csv file for writing
pbp_optical_data = open('pbp_optical.csv', 'wb')

# create a csv writer object and write the headers
csvwriter = csv.writer(pbp_optical_data)
pbp_optical_headers = ['season', 
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
                       'away_team_q2_score',
                       'away_team_q3_score',
                       'away_team_q4_score',
                       'home_team', 
                       'home_team_id',
                       'home_team_score',
                       'home_team_q1_score',
                       'home_team_q2_score',
                       'home_team_q3_score',
                       'home_team_q4_score',
                       'stadium',
                       'quarter',
                       'event_id',
                       'game_clock',
                       'time',
                       'player_id',
                       'global_player_id',
                       'pbp_seq_number',
                       'shot_clock'
                       ]
                   
csvwriter.writerow(pbp_optical_headers)

# before we traverse through the data, read in the common values needed for all rows                   
commonrows = []

for node in tree.iter('season'):
    commonrows.append(node.attrib.get('season'))
for node in tree.iter('gamecode'):
    commonrows.append(node.attrib.get('code'))
    commonrows.append(node.attrib.get('global-id'))
for node in tree.iter('game-type'):
    commonrows.append(node.attrib.get('id'))
    commonrows.append(node.attrib.get('description'))
for node in tree.iter('nba-boxscore'):
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
                if quarter.attrib.get('quarter') == '2':
                    commonrows.append(quarter.attrib.get('score'))
                if quarter.attrib.get('quarter') == '3':
                    commonrows.append(quarter.attrib.get('score'))
                if quarter.attrib.get('quarter') == '4':
                    commonrows.append(quarter.attrib.get('score'))
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
                if quarter.attrib.get('quarter') == '2':
                    commonrows.append(quarter.attrib.get('score'))
                if quarter.attrib.get('quarter') == '3':
                    commonrows.append(quarter.attrib.get('score'))
                if quarter.attrib.get('quarter') == '4':
                    commonrows.append(quarter.attrib.get('score'))
for node in tree.iter('stadium'):
    commonrows.append(node.attrib.get('name'))
    
# we have a list of all of the rows that will be the same
# now we need to traverse through and get all of the oncourt data

pbp_optical = []
for node in tree.iter('sequence-pbp'):
    quarter = node.attrib.get('period')
    for moment in node:
        pbp_optical.append(quarter)
        pbp_optical.append(moment.attrib.get('event-id'))
        pbp_optical.append(moment.attrib.get('game-clock'))
        pbp_optical.append(moment.attrib.get('time'))
        pbp_optical.append(moment.attrib.get('player-id'))
        pbp_optical.append(moment.attrib.get('global-player-id'))
        pbp_optical.append(moment.attrib.get('pbp-seq-number'))
        pbp_optical.append(moment.attrib.get('shot-clock'))
        csvwriter.writerow(commonrows + pbp_optical)
        pbp_optical = []

pbp_optical_data.close()