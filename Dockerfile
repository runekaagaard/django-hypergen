# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . /code/
WORKDIR /code/
RUN pip install -r requirements-prod.txt
RUN make cython-compile
EXPOSE 8000
WORKDIR /code/examples/
CMD PROD=1 python manage.py collectstatic --noinput
CMD PROD=1 gunicorn wsgi --bind 0.0.0.0:8000 --error-logfile - --log-level warn
