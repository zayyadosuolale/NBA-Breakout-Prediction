ALTER TABLE master_2024_25_clean
RENAME COLUMN G TO games_played,
RENAME COLUMN GS TO games_started,
RENAME COLUMN MP TO minutes_per_game,
RENAME COLUMN TRB TO rebounds_per_game,
RENAME COLUMN AST TO assists_per_game,
RENAME COLUMN STL TO steals_per_game,
RENAME COLUMN BLK TO blocks_per_game,
RENAME COLUMN pts TO points_per_game,
RENAME COLUMN PER TO per,
RENAME COLUMN USG_pct TO usage_pct,
RENAME COLUMN TS_pct TO true_shooting_pct,
RENAME COLUMN WS TO win_shares,
RENAME COLUMN BPM TO Box_PlusMinus,
RENAME COLUMN vorp TO vorp,
RENAME COLUMN pos TO position;

ALTER TABLE master_2020_21_clean
RENAME COLUMN BPM TO Box_PlusMinus;

select*
from master_2020_21_clean

-- Changed each column name in the table to be more descriptive
