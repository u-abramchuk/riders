FROM python:3.6

COPY . /app

WORKDIR /app

RUN pip install -r requirements

ENV APP_SETTINGS="production"

EXPOSE 5000

ENTRYPOINT ["python", "run.py" ]
