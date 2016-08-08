drop table if exists test.box_optical_possessions;
create table test.box_optical_possessions
(
season int, 
gamecode int, 
game_id int, 
gametype_id int, 
gametype varchar(50), 
gamedate varchar(50), 
gametime varchar(50), 
away_team varchar(50),
away_team_id varchar(50),
away_team_score int,
away_team_q1_score int,
away_team_q2_score int,
away_team_q3_score int,
away_team_q4_score int,
home_team varchar(50), 
home_team_id varchar(50),
home_team_score int,
home_team_q1_score int,
home_team_q2_score int,
home_team_q3_score int,
home_team_q4_score int,
stadium varchar(50),
team_alias varchar(50),
team_global_id varchar(50),
team_id varchar(50),
time_start varchar(50),
time_end varchar(50),
start_timestamp double,
end_timestamp double,
possession_length varchar(50),
touches int,
passes int,
dribbles int,
result varchar(50),
points int
);
#drop table nba.stats_totals;
# delete from nba.stats_totals where Season <= 2014;

LOAD DATA LOCAL INFILE 'D:\\Basketball\\pistons\\box_optical_possessions.csv' 
INTO TABLE test.box_optical_possessions
COLUMNS TERMINATED BY ','
ignore 1 lines;

select team,
result,
possessions,
round(touches/possessions,1) as touches_per_poss,
round(passes/possessions,1) as passes_per_poss,
round(dribbles/possessions,1) as dribbles_per_poss
from
(
SELECT 
team_alias as team, 
result, 
count(*) as possessions,
sum(touches) as touches,
sum(passes) as passes,
sum(dribbles) as dribbles

from test.box_optical_possessions

group by 1,2
) a

group by 1,2

union

select team,
'Total' as result,
possessions,
round(touches/possessions,1) as touches_per_poss,
round(passes/possessions,1) as passes_per_poss,
round(dribbles/possessions,1) as dribbles_per_poss
from
(
SELECT 
team_alias as team, 
count(*) as possessions,
sum(touches) as touches,
sum(passes) as passes,
sum(dribbles) as dribbles

from test.box_optical_possessions

group by 1
) a

group by 1,2;