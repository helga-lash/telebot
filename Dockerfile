FROM python:3.12.2-alpine3.19  as base
LABEL authors="Mikhail Fomenko"
RUN pip install --upgrade pip
RUN mkdir /log /conf /reports
COPY helpers_entity/requirements/common.txt /requirements/helpers.txt
COPY requirements/common.txt /requirements/common.txt
COPY app /app
COPY helpers_entity/helpers /app/helpers
COPY configuration-example.yaml /conf/example.yaml

#FROM base as unit-tests
#COPY requirements/unit-tests.txt /requirements/unit-tests.txt
#RUN pip install -r /requirements/unit-tests.txt
#COPY tests/unit_tests /app/unit_tests
#COPY tests/utests.py /app/utests.py
#WORKDIR /app
#ENTRYPOINT ["python3", "/app/utests.py"]