CREATE VIEW fazile.views AS
SELECT
    title,
    views,
    rank,
    date,
    from_iso8601_timestamp(retrieved_at) AS retrieved_at
FROM fazile.raw_views
ORDER BY
    date ASC,
    rank ASC;
