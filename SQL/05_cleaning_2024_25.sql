DROP TABLE IF EXISTS master_2024_25 ;
Create table master_2024_25
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
        `clean24-25` r
        join `advclean24-25` a
        on r.player = a.player and
        r.season = a.season and
        r.team = a.team;
        


create temporary table playerswith2_4 as
select distinct player,season
from master_2024_25
where team = '2TM';

DELETE m
FROM master_2024_25 m
JOIN playerswith2_4 p
  ON m.Player = p.Player
 AND m.Season = p.Season
WHERE m.Team <> '2TM';

-- DELETING 3TM DUPLICATES
create temporary table playerswith3_3 as
select distinct player,season
from master_2024_25
where team = '3TM';

DELETE m
FROM master_2024_25 m
JOIN playerswith3_3 p
  ON m.Player = p.Player
 AND m.Season = p.Season
WHERE m.Team <> '3TM';

select*
from master_2024_25
where team like '%3TM%';

select*
from master_2024_25
where player like '%marjon%';

