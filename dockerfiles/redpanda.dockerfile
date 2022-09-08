FROM vectorized/redpanda:v22.1.4-amd64 as redpanda
RUN rpk config set redpanda.auto_create_topics_enabled true