{{
    config(
        materialized='view'
    )
}}


with tripdata as 
(
    select * from {{ source('staging', 'fhv_tripdata') }}
    where dispatching_base_num is not null
)
select
     -- identifiers
    cast(dispatching_base_num as string) as dispatching_base_num,
    cast(pulocationid as integer) as pulocationid,
    cast(dolocationid as integer) as dolocationid,

    -- timestamps
    TIMESTAMP_MILLIS(pickup_datetime) as pickup_datetime_st,
    TIMESTAMP_MILLIS(dropoff_datetime) as dropoff_datetime_st,
    pickup_datetime,
    dropoff_datetime,

    -- trip info
    sr_flag,
    affiliated_base_number

from tripdata



-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}

