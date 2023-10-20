FROM python:3.12

WORKDIR /app

COPY ../requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY .. .

VOLUME ["/app"]

CMD ["python3","webapp.py"]