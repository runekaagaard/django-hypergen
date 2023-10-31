# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . /code/
WORKDIR /code/
RUN pip install -r requirements-prod.txt
RUN make cython-compile
EXPOSE 8000
WORKDIR /code/examples/
# CMD gunicorn wsgi --bind 0.0.0.0:8000 --error-logfile - --log-level warn --workers 4 --max-requests 100000 --max-requests-jitter 1000
CMD daphne --bind 0.0.0.0 -p 8000 --access-log - --verbosity 1 asgi:application
