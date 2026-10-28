-- Schema mirrors the parquet dtypes. \copy streams the file through psql into the
-- server one buffer at a time; neither side ever holds the whole file.
DROP TABLE IF EXISTS trips;
CREATE TABLE trips (
  vendor_id             integer,
  tpep_pickup_datetime  timestamp,
  tpep_dropoff_datetime timestamp,
  passenger_count       double precision,
  trip_distance         double precision,
  ratecode_id           double precision,
  store_and_fwd_flag    text,
  pu_location_id        integer,
  do_location_id        integer,
  payment_type          bigint,
  fare_amount           double precision,
  extra                 double precision,
  mta_tax               double precision,
  tip_amount            double precision,
  tolls_amount          double precision,
  improvement_surcharge double precision,
  total_amount          double precision,
  congestion_surcharge  double precision,
  airport_fee           double precision
);

\copy trips FROM '/data/yellow_tripdata_2024-01.csv' WITH (FORMAT csv, HEADER true)

-- Sets hint bits and the visibility map now. Without it the FIRST query after the
-- load rewrites every page, and those writes inflate the peak measured in the demo.
VACUUM ANALYZE trips;
