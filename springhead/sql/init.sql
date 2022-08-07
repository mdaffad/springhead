CREATE MATERIALIZED SOURCE IF NOT EXISTS user_signups (
   email varchar,
)
WITH (
   'connector'='kafka',
   'kafka.topic'='user_signups',
   'kafka.brokers'='redpanda:29092',
   'kafka.scan.startup.mode'='latest',
   'kafka.consumer.group'='demo_consumer_name'
)
ROW FORMAT JSON;

CREATE MATERIALIZED VIEW user_signups_ctr AS
SELECT
   email
FROM
   user_signups;