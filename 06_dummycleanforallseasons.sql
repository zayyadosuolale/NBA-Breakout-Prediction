CREATE TABLE master_2020_21_clean
like master_2020_21;

insert into master_2020_21_clean
select*
from master_2020_21;

CREATE TABLE master_2021_22_clean
like master_2021_22;

insert into master_2021_22_clean
select*
from master_2021_22;

CREATE TABLE master_2022_23_clean
like master_2022_23;

insert into master_2022_23_clean
select*
from master_2022_23;

CREATE TABLE master_2023_24_clean
like master_2023_24;

insert into master_2023_24_clean
select*
from master_2023_24;

CREATE TABLE master_2024_25_clean
like master_2024_25;

insert into master_2024_25_clean
select*
from master_2024_25;

select count(*)
from 
master_2023_24;

select *
from master_2023_24_clean

