Drop table if Exists nba_master_all;
Create table nba_master_all
SELECT * FROM master_2020_21_clean
UNION ALL
SELECT * FROM master_2021_22_clean
UNION ALL
SELECT * FROM master_2022_23_clean
UNION ALL
SELECT * FROM master_2023_24_clean
UNION ALL
SELECT * FROM master_2024_25_clean;
select*
from nba_master_all
where player like '%Wemba%';

SELECT player, season, COUNT(*) AS row_count
FROM nba_master_all
GROUP BY player, season
HAVING COUNT(*) > 1;

Alter table nba_master_all
Rename column vorp to value_over_replacement;