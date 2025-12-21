CREATE EXTERNAL TABLE IF NOT EXISTS fazile.raw_views (
    title STRING,
    views INT,
    rank INT,
    date DATE,
    retrieved_at STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://fazile-wikidata/raw-views/';

