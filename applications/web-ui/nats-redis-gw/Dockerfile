FROM python:3.8-alpine

RUN pip install -U pip && pip install asyncio-nats-client==0.11.4 redis==3.5.3 protobuf==3.15.8
RUN mkdir /nats-redis-gw
WORKDIR /nats-redis-gw
COPY config.py run.py datastream_pb2.py ./

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN chown appuser:appgroup -R /nats-redis-gw
USER appuser

ENTRYPOINT ["python", "run.py"]
