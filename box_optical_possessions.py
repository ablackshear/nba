# This code will parse the play by play optical tracking SportVU XML files and output a CSV file

import xml.etree.ElementTree as etree
import csv

# parse the entire file
tree = etree.parse('D:\Basketball\pistons\sportsvu\NBA_FINALBOX_OPTICAL$2016060209.XML')

# open a csv file for writing
box_optical_data = open('box_optical_possessions.csv', 'wb')

# create a csv writer object and write the headers
csvwriter = csv.writer(box_optical_data)
box_optical_headers = ['season', 
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
                       'team_alias',
                       'team_global_id',
                       'team_id',
                       'time_start',
                       'time_end',
                       'start_timestamp',
                       'end_timestamp',
                       'possession_length',
                       'touches',
                       'passes',
                       'dribbles',
                       'result',
                       'points'
                       ]
                   
csvwriter.writerow(box_optical_headers)

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
# now we need to traverse through and get all of the other data

box_optical = []
for node in tree.iter('possessions'):
    for qtr in node:
        quarter = node.attrib.get('number')
        for poss in qtr:
            box_optical.append(poss.attrib.get('team-alias'))
            box_optical.append(poss.attrib.get('team-global-id'))
            box_optical.append(poss.attrib.get('team-id'))
            box_optical.append(poss.attrib.get('time-start'))
            box_optical.append(poss.attrib.get('time-end'))
            box_optical.append(poss.attrib.get('start-timestamp'))
            box_optical.append(poss.attrib.get('end-timestamp'))
            box_optical.append(poss.attrib.get('possession-length'))
            box_optical.append(poss.attrib.get('touches'))
            box_optical.append(poss.attrib.get('passes'))
            box_optical.append(poss.attrib.get('dribbles'))
            box_optical.append(poss.attrib.get('result'))
            box_optical.append(poss.attrib.get('points'))
            csvwriter.writerow(commonrows + box_optical)
            box_optical = []

box_optical_data.close()