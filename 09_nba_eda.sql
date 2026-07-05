---- DATA ANALYSIS
---------------------------------------
--  SECTION 1 LEAGUE TRENDS
-- Purpose: Examine how league-wide player performance has changed from
-- 2020-21 through 2024-25.

-- Methodology:
-- Rotation players are defined as players averaging  at least 12.0 minutes per game.

--- Number of unique players each season ----

select season, count(distinct player) as num_uniqueplayers_eachseason
from 
nba_master_all
group by season;
SELECT
    SUM(games_played >= 35) AS over_35,
    SUM(games_played >= 50) AS over_50,
    SUM(games_played >= 65) AS over_65,
    COUNT(*) AS total
FROM nba_master_all;

-- Why did I choose above 35 games played
#35 games played keeps above 50% of all player records and makes sense for league leaderboads
-------------------------------------------------------------------------------------------
SELECT
    COUNT(*) AS total_players,
    SUM(minutes_per_game >= 12) AS rotation_players
FROM nba_master_all;

-- Choosing 12 min cutoff for a rotational player
# Rotation players were defined as averaging at least 12.0 minutes per game. 
# This threshold retained approximately 74% of all player-season observations 
# while excluding low-minute players whose advanced metrics can be unstable due to limited playing time.

-- League Average Age by Season (Rotation Players, 12+ MPG)
select season, round(avg(age) ,2) as avg_age_season
from
nba_master_all
where minutes_per_game >= 12
group by season
order by avg(age) desc;

-- League Average Points Per Game by Season (Rotation Players, 12+ MPG)
 select season, round(avg(points_per_game),2) as avg_ppg_season
 from nba_master_all
 where minutes_per_game >= 12
 group by season
order by avg_ppg_season desc;

-- League Average Box Plus-Minus by Season (Rotation Players, 12+ MPG)
select season, round(avg(box_plusminus),2) as avg_bpm_season
 from nba_master_all
 where minutes_per_game >= 12
 group by season
order by avg_bpm_season desc;

-- League Average True Shooting% by Season (Rotation Players, 12+ MPG)
select season, round(avg(true_shooting_pct),2) as avg_ts_season
 from nba_master_all
 where minutes_per_game > 12 
 group by season
order by avg_ts_season desc;

-- League Average Usage_Pct by Season (Rotation Players, 12+ MPG)
select season, round(avg(usage_pct),2) as avg_usage_pct
 from nba_master_all
 where minutes_per_game > 12
 group by season
order by avg_usage_pct desc;
---------------------------------------------------------------------------------------------------------

-- Section 2 :LEAGUE LEADERS
-- Purpose: Identify the league's top performers in major statistical categories for each season.
-- Methodology:
-- • Minimum 12 MPG
-- • Minimum 35 Games Played
-- • Additional filters applied where appropriate
-- • ROW_NUMBER() used for rankings


-- Top 3 scorers each season 'Scoring leaders '
select player,season, points_per_game, Rank_n
from (
select player, season, points_per_game,minutes_per_game, games_played, row_number() over (partition by season order by points_per_game desc) as Rank_n
from
nba_master_all
where games_played >= 35 and minutes_per_game >= 12) t
where Rank_n <= 3
;

-- Top 3 BPM by Season (MPG >= 12)
select player,season, Box_PlusMinus,rank_num
from (
select player,season,minutes_per_game, box_plusminus, row_number() over (partition by season order by box_plusminus desc) as rank_num
from
nba_master_all
where minutes_per_game >= 12 and games_played >= 35) t
where rank_num <= 3 ;

-- Top 3 PER by Season (MPG >= 12)
select *
from (
select player, season, per, row_number() over (partition by season order by per desc) as Rank_n
from
nba_master_all
where minutes_per_game >= 12
and games_played >= 35
) t
where Rank_n <= 3;

-- Top 3 WIN SHARES by Season (MPG >= 12)
select *
from (
select player, season, win_shares, row_number() over (partition by season order by win_shares desc) as Rank_n
from
nba_master_all
where minutes_per_game >= 12
and games_played >= 35
) t
where Rank_n <= 3;

-- PURPOSE: Trying to find where the median points are to find meaningful ts%
SELECT
    COUNT(*) AS total_players,
    SUM(points_per_game >= 5) AS ppg_5,
    SUM(points_per_game >= 9) AS ppg_9,
    SUM(points_per_game >= 15) AS ppg_15,
    SUM(points_per_game >= 20) AS ppg_20
FROM nba_master_all
WHERE minutes_per_game >= 12;

-- PURPOSE: Trying to find where the median usg_pct is to find meaningful ts%
SELECT
    COUNT(*) AS total_players,
    SUM(usage_pct >= 13) AS usg_13,
    SUM(usage_pct >= 10) AS usg_10,
    SUM(usage_pct >= 18) AS usg_18,
    SUM(usage_pct >= 20) AS usg_20
FROM nba_master_all
WHERE minutes_per_game >= 12;
-- You score above 20 ppg that puts you in top 10% of the league
SELECT
    COUNT(*) AS total_players,
    SUM(points_per_game >= 20.5) AS usg_20
FROM nba_master_all
WHERE minutes_per_game >= 12;


-- Top 3 TS% by Season (MPG >= 12) and Points per game > 20 and usage_pct > 18
select *
from (
select player,season, true_shooting_pct, row_number() over (partition by season order by true_shooting_pct desc) as Rank_n
from
nba_master_all
where minutes_per_game >= 12
and games_played >= 35
and points_per_game > 20
and usage_pct > 18
) t
where Rank_n <= 3;

-- Top 3 USG_pct by Season (MPG >= 12) 
select *
from (
select player,season, usage_pct, row_number() over (partition by season order by usage_pct desc) as Rank_n
from
nba_master_all
where minutes_per_game >= 12 and games_played >=35
) t
where Rank_n <= 3;

-- Top 3 VORP by Season (MPG >= 12) 
select *
from (
select player,season, value_over_replacement, row_number() over (partition by season order by value_over_replacement desc) as Rank_n
from
nba_master_all
where minutes_per_game >= 12 and games_played >=35
) t
where Rank_n <= 3;

---------------------------------------------------------------------------------------------------------------------------------------------------

-- Section 3 : Young Players (Age 24)
-- **NOTE On Baskteball Reference a player's age for a given season is calculated as their age on February 1 of that season
-- Purpose: Identify the league's top-performing young players.
-- Methodology:
-- • Age < 24
-- • Same filters used in League Leaders

-- Young Player Experience Distribution (Age <= 24)
Select player,  MIN(age) AS youngest_age_in_dataset, 
max(age) as oldest_age
,count(distinct season) as seasons_played
from nba_master_all
where age <= 24
group by player
order by seasons_played desc;

select 
case 
 When seasons_played >= 4 Then '4+ Seasons'
 When seasons_played >= 3 Then '3 Seasons'
 WHEN seasons_played = 2 THEN '2 seasons'
 ELSE '1 season'
end as experience_level
 , COUNT(*) AS player_count
from
( 
select
 player, count(distinct season) as seasons_played
 from nba_master_all
 where age <= 24
 group by player) t
 group by experience_level
 order by experience_level;
-- Young Players with the most seasons played in this dataset
select *
from
(
select player, count(distinct season) as seasons_played
from
nba_master_all
where age <= 24
group by player
)t
order by seasons_played desc;
-- Players averaged around 2 full seasons in this data set played before turning 25
select round(avg(seasons_played),2) as avg_seasons_played_before_25
from(
select count(distinct season) as seasons_played
from
nba_master_all
where age <= 24
group by player) t;
-----------------------------------------------------------------------------------

-- Top 3 young scorers each season 'Scoring leaders '
select player,season, points_per_game, Rank_n, age
from (
select player, season, age ,points_per_game,minutes_per_game, games_played, row_number() over (partition by season order by points_per_game desc) as Rank_n
from
nba_master_all
where games_played >= 35 and minutes_per_game >= 12 and age <= 24 ) t
where Rank_n <= 3
;

-- Top 3 young BPM by Season (MPG >= 12)
select player,season, Box_PlusMinus,rank_num, age
from (
select player,season,minutes_per_game,age, box_plusminus, row_number() over (partition by season order by box_plusminus desc) as rank_num
from
nba_master_all
where minutes_per_game >= 12 and games_played >= 35 and age <=24) t
where rank_num <= 3 ;

-- Top 3 young PER by Season (MPG >= 12)
select *
from (
select player, season, per,age, row_number() over (partition by season order by per desc) as Rank_n
from
nba_master_all
where minutes_per_game >= 12
and games_played >= 35
and age <= 24
) t
where Rank_n <= 3;


-- TOP 3 Young Win Shares player by Season (age < 24)
select *
from (
select player ,age, season, win_shares, row_number() over (partition by season order by win_shares desc) as Rank_n
from nba_master_all
where minutes_per_game >= 12 and 
games_played >= 35
and age <=24
)t
where rank_n <=3;

-- Top 3 TS% by Season (MPG >= 12) and Points per game > 20 and usage_pct > 18 for young player
select *
from (
select player,age, season, true_shooting_pct, row_number() over (partition by season order by true_shooting_pct desc) as Rank_n
from
nba_master_all
where minutes_per_game >= 12
and games_played >= 35
and points_per_game > 20
and usage_pct > 18
and age <= 24
) t
where Rank_n <= 3;

-- Top 3 USG_pct by Season (MPG >= 12) 
select *
from (
select player, age, season, usage_pct, row_number() over (partition by season order by usage_pct desc) as Rank_n
from
nba_master_all
where minutes_per_game >= 12 and games_played >= 35 and age <= 24
) t
where Rank_n <= 3;

-- Top 3 VORP by Season (MPG >= 12) 
select *
from (
select player, age , season, value_over_replacement, row_number() over (partition by season order by value_over_replacement desc) as Rank_n
from
nba_master_all
where minutes_per_game >= 12 and games_played >= 35 and age <= 24
) t
where Rank_n <= 3;

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Section 4 Distributional Stats

-- Purpose: Find the avg stats sorted by age and position
-- Methodology: Filters as needed
-- AVG STATS FOR A ROTATIONAL 
SELECT
    round (AVG(points_per_game), 2) as  avg_point_per_game,
    round(AVG(box_plusminus),2) as avg_bpm,
    round(AVG(rebounds_per_game),2) as avg_rbg,
    round(AVG(assists_per_game),2) as avg_apg,
    round(AVG(steals_per_game),2) as avg_spg,
    round(AVG(blocks_per_game),2) as avg_bpg,
    round(AVG(usage_pct),2) as avg_usgpct,
    round(AVG(true_shooting_pct),2) as avg_tsp,
    round(AVG(win_shares),2) as avg_ws,
    round(AVG(value_over_replacement),2) as avg_vorp,
    round(AVG(per),2) as avg_per
FROM nba_master_all
where minutes_per_game >= 12;

-- STATS DISTRIBUTION BY AGES
SELECT
    age,
    round (AVG(points_per_game), 2) as  avg_point_per_game,
    round(AVG(box_plusminus),2) as avg_bpm,
    round(AVG(rebounds_per_game),2) as avg_rbg,
    round(AVG(assists_per_game),2) as avg_apg,
    round(AVG(steals_per_game),2) as avg_spg,
    round(AVG(blocks_per_game),2) as avg_bpg,
    round(AVG(usage_pct),2) as avg_usgpct,
    round(AVG(true_shooting_pct),2) as avg_tsp,
    round(AVG(win_shares),2) as avg_ws,
    round(AVG(value_over_replacement),2) as avg_vorp,
    round(AVG(per),2) as avg_per
FROM nba_master_all
where minutes_per_game >= 12
GROUP BY age
order by age;

-- STATS DISTRIBUTION BY POSITIONS in 2020 - 2021
SELECT
    position,
    round (AVG(points_per_game), 2) as  avg_point_per_game,
    round(AVG(box_plusminus),2) as avg_bpm,
    round(AVG(rebounds_per_game),2) as avg_rbg,
    round(AVG(assists_per_game),2) as avg_apg,
    round(AVG(steals_per_game),2) as avg_spg,
    round(AVG(blocks_per_game),2) as avg_bpg,
    round(AVG(usage_pct),2) as avg_usgpct,
    round(AVG(true_shooting_pct),2) as avg_tsp,
    round(AVG(win_shares),2) as avg_ws,
    round(AVG(value_over_replacement),2) as avg_vorp,
    round(AVG(per),2) as avg_per
FROM nba_master_all
where minutes_per_game >= 12
and season like '%2020-21%'
GROUP BY position
order by position;

-- STATS DISTRIBUTION BY POSITIONS in 2021 - 2022
SELECT
    position,
    round (AVG(points_per_game), 2) as  avg_point_per_game,
    round(AVG(box_plusminus),2) as avg_bpm,
    round(AVG(rebounds_per_game),2) as avg_rbg,
    round(AVG(assists_per_game),2) as avg_apg,
    round(AVG(steals_per_game),2) as avg_spg,
    round(AVG(blocks_per_game),2) as avg_bpg,
    round(AVG(usage_pct),2) as avg_usgpct,
    round(AVG(true_shooting_pct),2) as avg_tsp,
    round(AVG(win_shares),2) as avg_ws,
    round(AVG(value_over_replacement),2) as avg_vorp,
    round(AVG(per),2) as avg_per
FROM nba_master_all
where minutes_per_game >= 12
and season like '%2021-22%'
GROUP BY position
order by position;

-- STATS DISTRIBUTION BY POSITIONS in 2022 - 2023
SELECT
    position,
    round (AVG(points_per_game), 2) as  avg_point_per_game,
    round(AVG(box_plusminus),2) as avg_bpm,
    round(AVG(rebounds_per_game),2) as avg_rbg,
    round(AVG(assists_per_game),2) as avg_apg,
    round(AVG(steals_per_game),2) as avg_spg,
    round(AVG(blocks_per_game),2) as avg_bpg,
    round(AVG(usage_pct),2) as avg_usgpct,
    round(AVG(true_shooting_pct),2) as avg_tsp,
    round(AVG(win_shares),2) as avg_ws,
    round(AVG(value_over_replacement),2) as avg_vorp,
    round(AVG(per),2) as avg_per
FROM nba_master_all
where minutes_per_game >= 12
and season like '%2022-23%'
GROUP BY position
order by position;
-- STATS DISTRIBUTION BY POSITIONS in 2023 - 2024
SELECT
    position,
    round (AVG(points_per_game), 2) as  avg_point_per_game,
    round(AVG(box_plusminus),2) as avg_bpm,
    round(AVG(rebounds_per_game),2) as avg_rbg,
    round(AVG(assists_per_game),2) as avg_apg,
    round(AVG(steals_per_game),2) as avg_spg,
    round(AVG(blocks_per_game),2) as avg_bpg,
    round(AVG(usage_pct),2) as avg_usgpct,
    round(AVG(true_shooting_pct),2) as avg_tsp,
    round(AVG(win_shares),2) as avg_ws,
    round(AVG(value_over_replacement),2) as avg_vorp,
    round(AVG(per),2) as avg_per
FROM nba_master_all
where minutes_per_game >= 12
and season like '%2023-24%'
GROUP BY position
order by position;

-- STATS DISTRIBUTION BY POSITIONS in 2024 - 2025
SELECT
    position,
    round (AVG(points_per_game), 2) as  avg_point_per_game,
    round(AVG(box_plusminus),2) as avg_bpm,
    round(AVG(rebounds_per_game),2) as avg_rbg,
    round(AVG(assists_per_game),2) as avg_apg,
    round(AVG(steals_per_game),2) as avg_spg,
    round(AVG(blocks_per_game),2) as avg_bpg,
    round(AVG(usage_pct),2) as avg_usgpct,
    round(AVG(true_shooting_pct),2) as avg_tsp,
    round(AVG(win_shares),2) as avg_ws,
    round(AVG(value_over_replacement),2) as avg_vorp,
    round(AVG(per),2) as avg_per
FROM nba_master_all
where minutes_per_game >= 12
and season like '%2024-25%'
GROUP BY position
order by position;




