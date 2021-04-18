FROM python:3.8-alpine

COPY requirements.txt ./
RUN pip install -U pip && pip install -r requirements.txt

RUN mkdir /web-ui
WORKDIR /web-ui
COPY app /web-ui/app
COPY run.py gunicorn-cfg.py config.py ./


RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN chown appuser:appgroup -R /web-ui
USER appuser

EXPOSE 8080
ENTRYPOINT ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]