{{ config(
    materialized='table',
    schema='silver'
) }}

with source_data as (

    select
        title,
        price,
        year,
        city,
        mileage,
        posted_time,
        listing_url,
        scraped_at,
        loaded_at
    from bronze.riyasewana_listings_raw

),

cleaned as (

    select
        title,

        nullif(
            regexp_replace(price::text, '[^0-9]', '', 'g'),
            ''
        )::bigint as price_lkr,

        nullif(
            regexp_replace(year::text, '[^0-9]', '', 'g'),
            ''
        )::int as year,

        city,

        nullif(
            regexp_replace(mileage::text, '[^0-9]', '', 'g'),
            ''
        )::int as mileage_km,

        posted_time,
        listing_url,

        scraped_at::timestamp as scraped_at,
        loaded_at::timestamp as loaded_at

    from source_data

)

select *
from cleaned
where listing_url is not null