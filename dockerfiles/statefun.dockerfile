FROM apache/flink-statefun:3.2.0

RUN mkdir -p /opt/statefun/modules/remote

COPY springhead/module.yaml /opt/statefun/modules/remote/module.yaml