# This code will parse the raw SportVU movement data XML files and create a CSV file

import xml.etree.ElementTree as etree
import csv

# initialize the file names

file1 = 'D:\Basketball\pistons\sportsvu\NBA_FINAL_SEQUENCE_OPTICAL$2016060209_Q1.XML'
file2 = 'D:\Basketball\pistons\sportsvu\NBA_FINAL_SEQUENCE_OPTICAL$2016060209_Q2.XML'
file3 = 'D:\Basketball\pistons\sportsvu\NBA_FINAL_SEQUENCE_OPTICAL$2016060209_Q3.XML'
file4 = 'D:\Basketball\pistons\sportsvu\NBA_FINAL_SEQUENCE_OPTICAL$2016060209_Q4.XML'

# open a csv file for writing
optical_data = open('optical_data.csv', 'wb')

# create a csv writer object and write the headers
csvwriter = csv.writer(optical_data)
optical_headers = ['season', 
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
                   'gameclock',
                   'time',
                   'shotclock',
                   'ball_team_id',
                   'ball_id',
                   'ball_x_loc',
                   'ball_y_loc',
                   'ball_z_loc',
                   'player1_team_id',
                   'player1_id',
                   'player1_x_loc',
                   'player1_y_loc',
                   'player1_z_loc',
                   'player2_team_id',
                   'player2_player_id',
                   'player2_x_loc',
                   'player2_y_loc',
                   'player2_z_loc',
                   'player3_team_id',
                   'player3_player_id',
                   'player3_x_loc',
                   'player3_y_loc',
                   'player3_z_loc',
                   'player4_team_id',
                   'player4_player_id',
                   'player4_x_loc',
                   'player4_y_loc',
                   'player4_z_loc',
                   'player5_team_id',
                   'player5_player_id',
                   'player5_x_loc',
                   'player5_y_loc',
                   'player5_z_loc',
                   'player6_team_id',
                   'player6_player_id',
                   'player6_x_loc',
                   'player6_y_loc',
                   'player6_z_loc',
                   'player7_team_id',
                   'player7_player_id',
                   'player7_x_loc',
                   'player7_y_loc',
                   'player7_z_loc',
                   'player8_team_id',
                   'player8_player_id',
                   'player8_x_loc',
                   'player8_y_loc',
                   'player8_z_loc',
                   'player9_team_id',
                   'player9_player_id',
                   'player9_x_loc',
                   'player9_y_loc',
                   'player9_z_loc',
                   'player10_team_id',
                   'player10_player_id',
                   'player10_x_loc',
                   'player10_y_loc',
                   'player10_z_loc'
                   ]

csvwriter.writerow(optical_headers)

# Function to process files, since we have multiple versions for each quarter
def process_file(filename):

    tree = etree.parse(filename)                   
                   
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
    # now we need to traverse through and get all of the tracking data
    
    optical = []
    for node in tree.iter('sequences'):
        quarter = node.attrib.get('period')
        for moment in node:
            optical.append(quarter)
            optical.append(moment.attrib.get('game-clock'))
            optical.append(moment.attrib.get('time'))
            optical.append(moment.attrib.get('shot-clock'))
            locations = moment.attrib.get('locations').split(';')
            # some of the records are missing the ball, so you need to check the size of the list
            # if the ball is missing the list only has 10 items, so I just fill it in with dummy data
            if len(locations) == 11:
                locations_split = locations[0].split(',')+locations[1].split(',')+locations[2].split(',')+locations[3].split(',')+locations[4].split(',')+locations[5].split(',')+locations[6].split(',')+locations[7].split(',')+locations[8].split(',')+locations[9].split(',')+locations[10].split(',')
            elif len(locations) == 10:   
                locations_split = ['-1','-1','0','0','0']+ locations[0].split(',')+locations[1].split(',')+locations[2].split(',')+locations[3].split(',')+locations[4].split(',')+locations[5].split(',')+locations[6].split(',')+locations[7].split(',')+locations[8].split(',')+locations[9].split(',')
            optical = optical + locations_split
            csvwriter.writerow(commonrows + optical)
            optical = []
            locations = []
            locations_split = []

process_file(file1)
process_file(file2)
process_file(file3)
process_file(file4)

optical_data.close()
    