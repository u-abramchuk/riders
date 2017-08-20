FROM python:3.6

COPY . /app

WORKDIR /app

RUN pip install -r requirements

ENV APP_SETTINGS="../config/development.config"

EXPOSE 5000

ENTRYPOINT ["python", "run.py" ]
