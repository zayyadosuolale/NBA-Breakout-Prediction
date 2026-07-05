-- CREATING DUMMY TABLE JOINING BASED ON THE STATS I NEED
DROP TABLE IF EXISTS master_2021_22 ;
Create table master_2021_22
 select r.player,
		r.season,
		r.age,
        r.team,
        r.pos,
        r.G,
        r.Gs,
        r.MP,
        r.TRB,
        r.AST,
        r.STL,
        r.BLK,
        r.pts,
        a.PER,
        a.USG_pct,
        a. TS_pct,
        a.WS,
        a.BPM,
        a.vorp
        from
        `clean21-22` r
        join `advclean21-22` a
        on r.player = a.player and
        r.season = a.season and
        r.team = a.team;


-- DELETING 2 TEAM DUPLICATES
create temporary table playerswith2_1 as
select distinct player,season
from master_2021_22
where team = '2TM';

DELETE m
FROM master_2021_22 m
JOIN playerswith2_1 p
  ON m.Player = p.Player
 AND m.Season = p.Season
WHERE m.Team <> '2TM';

select*
from master_2021_22
where team like '%4TM%';

-- DELETING 3TM DUPLICATES
create temporary table playerswith3_1 as
select distinct player,season
from master_2021_22
where team = '3TM';

DELETE m
FROM master_2021_22 m
JOIN playerswith3_1 p
  ON m.Player = p.Player
 AND m.Season = p.Season
WHERE m.Team <> '3TM';

-- DELETING 4TM DUPLICATES
create temporary table playerswith4_1 as
select distinct player,season
from master_2021_22
where team = '4TM';

DELETE m
FROM master_2021_22 m
JOIN playerswith4_1 p
  ON m.Player = p.Player
 AND m.Season = p.Season
WHERE m.Team <> '4TM';

select*
from master_2021_22
where player like '%Juancho%'

