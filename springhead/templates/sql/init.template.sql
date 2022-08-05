CREATE MATERIALIZED SOURCE IF NOT EXISTS {{stream_topic}} (
   email varchar,
)
WITH (
   'connector'='kafka',
   'kafka.topic'='{{stream_topic}}',
   'kafka.brokers'='redpanda:29092',
   'kafka.scan.startup.mode'='latest',
   'kafka.consumer.group'='{{stream_group}}'
)
ROW FORMAT JSON;

CREATE MATERIALIZED VIEW {{stream_topic}}_view AS
SELECT
   email
FROM
   {{stream_topic}};