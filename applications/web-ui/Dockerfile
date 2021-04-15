FROM python:3.8-alpine

RUN apk --update add redis supervisor

COPY requirements.txt ./
RUN pip install -U pip && pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY app /app/app
COPY nats /app/nats
COPY run.py gunicorn-cfg.py config.py supervisord.conf ./


RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN chown appuser:appgroup -R /app
USER appuser

EXPOSE 8080
ENTRYPOINT ["supervisord", "-c", "/app/supervisord.conf"]