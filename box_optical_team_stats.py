# This code will parse the play by play optical tracking SportVU XML files and output a CSV file

import xml.etree.ElementTree as etree
import csv

# parse the entire file
tree = etree.parse('D:\Basketball\pistons\sportsvu\NBA_FINALBOX_OPTICAL$2016060209.XML')

# open a csv file for writing
box_optical_data = open('box_optical_team_stats.csv', 'wb')

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
                       'team',
                       'feet',
                       'miles',
                       'meters',
                       'kilometers',
                       'offense_ft',
                       'offense_miles',
                       'offense_meters',
                       'offense_km',
                       'defense_ft',
                       'defense_miles',
                       'defense_meters',
                       'defense_km',
                       'kilometers-per-hour',
                       'miles-per-hour',
                       'off_km_hr',
                       'off_miles_hr',
                       'def_km_hr',
                       'def_miles_hr',
                       'away_touches',
                       'frequency',
                       'touch-frequency-pct',
                       'points-per-poss',
                       'fgatt',
                       'fgmade',
                       'fgpct',
                       '3patt',
                       '3pmade',
                       '3ppct',
                       'ftatt',
                       'ftmade',
                       'ftpct',
                       'ts_pct',
                       'assists',
                       'to-dead-ball',
                       'to-live-ball-pts-allow',
                       'to-live-ball',
                       'turnovers',
                       'to-dead-ball-pts-allow',
                       'offreb'
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
for node in tree.iter('team-stats'):
    if node.attrib.get('team') == 'visitors':
        box_optical = ['away']
        for stat in node:
            if stat.tag == 'distance-run':
                box_optical = box_optical + stat.attrib.values()
                for breakdown in stat:
                    if breakdown.attrib.get('breakdown') == 'offense':
                        box_optical = box_optical + breakdown.attrib.values()[1:]
                    if breakdown.attrib.get('breakdown') == 'defense':
                        box_optical = box_optical + breakdown.attrib.values()[1:]
            if stat.tag == 'average-speed':
                box_optical = box_optical + stat.attrib.values()
                for breakdown in stat:
                    if breakdown.attrib.get('breakdown') == 'offense':
                        box_optical = box_optical + breakdown.attrib.values()[1:]
                    if breakdown.attrib.get('breakdown') == 'defense':
                        box_optical = box_optical + breakdown.attrib.values()[1:]
            if stat.tag == 'possession-breakdown':
                for breakdown in stat:
                    poss_breakdown = []
                    if breakdown.attrib.get('touches') == '1':
                        poss_breakdown = box_optical + ['1']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
                    if breakdown.attrib.get('touches') == '2':
                        poss_breakdown = box_optical + ['2']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
                    if breakdown.attrib.get('touches') == '3':
                        poss_breakdown = box_optical + ['3']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
                    if breakdown.attrib.get('touches') == '4':
                        poss_breakdown = box_optical + ['4']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
                    if breakdown.attrib.get('touches') == '5':
                        poss_breakdown = box_optical + ['5']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
                    if breakdown.attrib.get('touches') == '6':
                        poss_breakdown = box_optical + ['6']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
                    if breakdown.attrib.get('touches') == '7':
                        poss_breakdown = box_optical + ['7']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
                    if breakdown.attrib.get('touches') == '8+':
                        poss_breakdown = box_optical + ['8+']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
    if node.attrib.get('team') == 'home':
        box_optical = ['home']
        for stat in node:
            if stat.tag == 'distance-run':
                box_optical = box_optical + stat.attrib.values()
                for breakdown in stat:
                    if breakdown.attrib.get('breakdown') == 'offense':
                        box_optical = box_optical + breakdown.attrib.values()[1:]
                    if breakdown.attrib.get('breakdown') == 'defense':
                        box_optical = box_optical + breakdown.attrib.values()[1:]
            if stat.tag == 'average-speed':
                box_optical = box_optical + stat.attrib.values()
                for breakdown in stat:
                    if breakdown.attrib.get('breakdown') == 'offense':
                        box_optical = box_optical + breakdown.attrib.values()[1:]
                    if breakdown.attrib.get('breakdown') == 'defense':
                        box_optical = box_optical + breakdown.attrib.values()[1:]
            if stat.tag == 'possession-breakdown':
                for breakdown in stat:
                    poss_breakdown = []
                    if breakdown.attrib.get('touches') == '1':
                        poss_breakdown = box_optical + ['1']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
                    if breakdown.attrib.get('touches') == '2':
                        poss_breakdown = box_optical + ['2']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
                    if breakdown.attrib.get('touches') == '3':
                        poss_breakdown = box_optical + ['3']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
                    if breakdown.attrib.get('touches') == '4':
                        poss_breakdown = box_optical + ['4']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
                    if breakdown.attrib.get('touches') == '5':
                        poss_breakdown = box_optical + ['5']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
                    if breakdown.attrib.get('touches') == '6':
                        poss_breakdown = box_optical + ['6']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
                    if breakdown.attrib.get('touches') == '7':
                        poss_breakdown = box_optical + ['7']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
                    if breakdown.attrib.get('touches') == '8+':
                        poss_breakdown = box_optical + ['8+']
                        for detail in breakdown:
                            poss_breakdown += detail.attrib.values()
                        csvwriter.writerow(commonrows + poss_breakdown)
box_optical_data.close()