FROM python:3.12.4-alpine3.20 AS base
LABEL authors="Mikhail Fomenko"
RUN pip install --upgrade pip
RUN mkdir /log /conf /reports
COPY helpers_entity/requirements/common.txt /requirements/helpers.txt
COPY requirements/common.txt /requirements/common.txt
COPY app /app
COPY helpers_entity/helpers /app/helpers
COPY helpers_entity/configuration-example.yaml /conf/example.yaml

FROM base AS prod
RUN pip install -r /requirements/common.txt
WORKDIR /app
ENTRYPOINT ["python3", "/app/telebot.py"]