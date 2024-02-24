{{
    config(
        materialized='view'
    )
}}

with tripdata as 
(
  select *,
        EXTRACT( year from CAST(pickup_datetime AS TIMESTAMP) ) as yr
  from {{ source('staging','fhv_tripdata') }}
)
select
    -- identifiers
    cast(dispatching_base_num as string) as dispatching_base_num,
    {{ dbt.safe_cast("pulocationid", api.Column.translate_type("integer")) }} as pickup_locationid,
    {{ dbt.safe_cast("dolocationid", api.Column.translate_type("integer")) }} as dropoff_locationid,
    
    -- timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropoff_datetime as timestamp) as dropoff_datetime,
    
    -- trip info
    cast(sr_flag as string) as sr_flag,
    cast(affiliated_base_number as string) as affiliated_base_number

from tripdata
where yr = 2019


-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
