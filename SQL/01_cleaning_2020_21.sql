--- MAKING SURE TABLE COPIED CORRECTLY
SELECT player, pts
FROM `clean20-21`
where Player like  'Giannis%' ;
SELECT player, pts
FROM `clean21-22`
where Player like  'Giannis%' ;
SELECT player, pts
FROM `clean23-24`
where Player like  'Giannis%' ;
SELECT player, pts
FROM `clean22-23`
where Player like  'Giannis%' ;
SELECT player, pts, season
FROM `clean24-25`
where Player like  'Giannis%' ;

SELECT *
FROM `clean21-22`
where Player like  'Giannis%' ;

SELECT *
FROM `advclean22-23`
where Player like  'Giannis%' ;

SELECT player, TS_pct, season
FROM `advclean23-24`
where Player like  'Giannis%' ;

SELECT *
FROM `advclean20-21`
where Player like  'Giannis%' ;

SELECT player, TS_pct, season
FROM `advclean24-25`
where Player like  'Giannis%' ;
-- END

-- CREATING DUMMY TABLE JOINING BASED ON THE STATS I NEED
DROP TABLE IF EXISTS master_2020_21 ;
Create table master_2020_21 
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
        r.PTS,
        a.PER,
        a.USG_pct,
        a. TS_pct,
        a.WS,
        a.BPM,
        a.vorp
        from
        `clean20-21` r
        join `advclean20-21` a
        on r.player = a.player and
        r.season = a.season and
        r.team = a.team;

-- HANDLING 2 or 3TM TEAM DUPLICATES
SELECT Player, Team, COUNT(*)
FROM `advclean20-21`
WHERE Player = 'Caris LeVert'
GROUP BY Player, Team;

SELECT Player, Team, COUNT(*)
FROM `clean20-21`
WHERE Player = 'Caris LeVert'
GROUP BY Player, Team;
-- END

-- DELETING 2 TEAM DUPLICATES
create temporary table playerswith2_1 as
select distinct player,season
from master_2020_21
where team = '2TM';

DELETE m
FROM master_2020_21 m
JOIN playerswith2 p
  ON m.Player = p.Player
 AND m.Season = p.Season
WHERE m.Team <> '2TM';
#This deletes the row when other related rows exist so player and season already exists so delete it and leave 2tm
-- END 

SELECT *
FROM master_2020_21
WHERE player like '%Harden';

SELECT *
FROM master_2020_21
WHERE player like '%Oladipo';


-- DELETING 3TM DUPLICATES
create temporary table playerswith3 as
select distinct player,season
from master_2020_21
where team = '3TM';

DELETE m
FROM master_2020_21 m
JOIN playerswith3 p
  ON m.Player = p.Player
 AND m.Season = p.Season
WHERE m.Team <> '3TM';

SELECT *
FROM master_2020_21
where team like '%3TM%';

        




