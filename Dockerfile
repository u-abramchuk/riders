FROM python:3.6

COPY .

RUN pip install -r requirements

ENTRYPOINT ["python", "run.py" ]
