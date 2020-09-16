FROM python:3.7-alpine

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
    AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}

RUN adduser -D admin

WORKDIR /home/website

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY website.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP website.py

RUN chown -R admin:admin ./
USER admin

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
