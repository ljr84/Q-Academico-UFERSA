FROM python:3.10-slim-buster
#FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
WORKDIR /usr/src/app
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=50002
#Server will reload itself on file changes if in dev mode
ENV FLASK_ENV=development 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]
