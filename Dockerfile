FROM python:3.6

COPY . /app

WORKDIR /app

RUN pip install -r requirements

ENV APP_SETTINGS="production"

ENTRYPOINT ["python", "run.py" ]
