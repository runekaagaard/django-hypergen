# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . /code/
WORKDIR /code/
RUN pip install -r examples/requirements.txt
RUN make cython-compile
EXPOSE 8000
WORKDIR /code/examples/
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
