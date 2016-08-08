# This code will parse the on-court stint SportVU XML files and output a CSV file

import xml.etree.ElementTree as etree
import csv

# parse the entire file
tree = etree.parse('D:\Basketball\pistons\sportsvu\NBA_FINAL_ONCOURT$2016060209.XML')

# open a csv file for writing
oncourt_data = open('oncourt.csv', 'wb')

# create a csv writer object and write the headers
csvwriter = csv.writer(oncourt_data)
oncourt_headers = ['league', 
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
                   'home_team', 
                   'home_team_id',
                   'oncourt_id', 
                   'home_player_id1',
                   'home_player_global_id1',
                   'home_player_name1',
                   'home_player_id2',
                   'home_player_global_id2', 
                   'home_player_name2',
                   'home_player_id3',
                   'home_player_global_id3', 
                   'home_player_name3',
                   'home_player_id4',
                   'home_player_global_id4', 
                   'home_player_name4',
                   'home_player_id5',
                   'home_player_global_id5', 
                   'home_player_name5',
                   'away_player_id1',
                   'away_player_global_id1',
                   'away_player_name1',
                   'away_player_id2',
                   'away_player_global_id2',
                   'away_player_name2',
                   'away_player_id3',
                   'away_player_global_id3',
                   'away_player_name3',
                   'away_player_id4',
                   'away_player_global_id4',
                   'away_player_name4',
                   'away_player_id5',
                   'away_player_global_id5',
                   'away_player_name5']
                   
csvwriter.writerow(oncourt_headers)

# before we traverse through the data, read in the game info
# The values that will be the same for all rows are:
# year, month, date, day, time, league ID, season, 
# visiting team alias, visiting team id, home team alias, home team id

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
for node in tree.iter('nba-oncourt-players'):
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
for node in tree.iter('home-team'):
    for child in node:
        if child.tag == 'team-name':
            commonrows.append(child.attrib.get('alias'))
        if child.tag =='team-code':
            commonrows.append(child.attrib.get('id'))

# we have a list of all of the rows that will be the same
# now we need to traverse through and get all of the oncourt data

oncourt = []
for node in tree.iter('oncourt'):
    oncourt_id = node.attrib.get('id')
    oncourt.append(oncourt_id)
    for team in node:
        if team.tag == 'visiting-team-players':
            for player in team:
                oncourt.append(player.attrib.get('id'))
                oncourt.append(player.attrib.get('global-id'))
                oncourt.append(player.attrib.get('display-name'))
        if team.tag == 'home-team-players':
            for player in team:
                oncourt.append(player.attrib.get('id'))
                oncourt.append(player.attrib.get('global-id'))
                oncourt.append(player.attrib.get('display-name'))
    csvwriter.writerow(commonrows + oncourt)
    oncourt = []

oncourt_data.close()