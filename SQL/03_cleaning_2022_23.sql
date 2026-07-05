DROP TABLE IF EXISTS master_2022_23 ;
Create table master_2022_23
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
        `clean22-23` r
        join `advclean22-23` a
        on r.player = a.player and
        r.season = a.season and
        r.team = a.team;
	
-- DELETING 2 TEAM DUPLICATES
create temporary table playerswith2_2 as
select distinct player,season
from master_2022_23
where team = '2TM';

DELETE m
FROM master_2022_23 m
JOIN playerswith2_2 p
  ON m.Player = p.Player
 AND m.Season = p.Season
WHERE m.Team <> '2TM';

select*
from master_2022_23
where player like '%Arcid%';