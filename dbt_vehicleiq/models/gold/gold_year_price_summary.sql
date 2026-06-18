{{ config(
    materialized='table'
) }}

select
    year,
    count(*) as total_listings,
    round(avg(price_lkr), 2) as average_price_lkr,
    min(price_lkr) as minimum_price_lkr,
    max(price_lkr) as maximum_price_lkr,
    round(avg(mileage_km), 2) as average_mileage_km
from {{ ref('silver_riyasewana_listings') }}
where year is not null
  and price_lkr is not null
group by year
order by year desc