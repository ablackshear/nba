drop table if exists test.pbp;
create table test.pbp 
(
league varchar(50), 
league_id int, 
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
away_team_q1_fouls int,
away_team_q2_score int,
away_team_q2_fouls int,
away_team_q3_score int,
away_team_q3_fouls int,
away_team_q4_score int,
away_team_q4_fouls int,
away_team_outcome varchar(50),
home_team varchar(50),
home_team_id varchar(50),
home_team_score int,
home_team_q1_score int,
home_team_q1_fouls int,
home_team_q2_score int,
home_team_q2_fouls int,
home_team_q3_score int,
home_team_q3_fouls int,
home_team_q4_score int,
home_team_q4_fouls int,
home_team_outcome varchar(50),
stadium varchar(50),
quarter int,
oncourt_id int,
time_minutes int,
time_seconds int,
pbp_id int,
global_player_id_1 int,
player_id_1 int,
display_name_1 varchar(50),
team_code_1 int,
team_alias_1 varchar(50),
global_player_id_2 int,
player_id_2 int,
display_name_2 varchar(50),
team_code_2 int ,
team_alias_2 varchar(50),
global_player_id_3 int,
player_id_3 int,
display_name_3 varchar(50),
team_code_3 int,
team_alias_3 varchar(50),
points_type int,
event_id int,
event_description varchar(50),
detail_id int,
detail_description varchar(50),
blocked varchar(50),
distance int,
x_shot_coord double,
y_shot_coord double,
fastbreak varchar(50),
in_paint varchar(50),
second_chance varchar(50),
off_turnover varchar(50),
player_score int,
player_fouls int,
visitor_score int,
home_score int,
visitor_fouls int,
home_fouls int,
position_id int,
position varchar(50),
textual_description varchar(100)
);

LOAD DATA LOCAL INFILE 'D:\\Basketball\\pistons\\pbp.csv' 
INTO TABLE test.pbp
COLUMNS TERMINATED BY ','
ignore 1 lines;

drop table if exists test.pbp_optical;
create table test.pbp_optical
(
season int, 
gamecode int, 
game_id int, 
gametype_id int, 
gametype varchar(50), 
gamedate varchar(50), 
gametime varchar(50), 
away_team varchar(50),
away_team_id int,
away_team_score int,
away_team_q1_score int,
away_team_q2_score int,
away_team_q3_score int,
away_team_q4_score int,
home_team varchar(50),  
home_team_id int,
home_team_score int,
home_team_q1_score int,
home_team_q2_score int,
home_team_q3_score int,
home_team_q4_score int,
stadium varchar(50),
quarter int,
event_id int,
game_clock double,
time double,
player_id int,
global_player_id int,
pbp_seq_number int,
shot_clock double
);

LOAD DATA LOCAL INFILE 'D:\\Basketball\\pistons\\pbp_optical.csv' 
INTO TABLE test.pbp_optical
COLUMNS TERMINATED BY ','
ignore 1 lines;

SELECT 
a.team_alias_1,
a.detail_description,
count(distinct pbp_id) as assisted_shots,
round(avg(a.distance),1) as avg_dist,
round(avg(shot_clock),1) as shot_clock,
sum(a.points_type) as pts


FROM test.pbp a inner join test.pbp_optical b
on a.pbp_id = b.pbp_seq_number

where a.textual_description like '%assist%'

group by 1,2;