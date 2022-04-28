# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY examples/requirements.txt /code/
RUN pip install -r requirements.txt
COPY examples /code/
RUN rm /code/hypergen
COPY src/hypergen /code/hypergen
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
