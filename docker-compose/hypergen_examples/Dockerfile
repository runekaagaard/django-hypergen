FROM python:3.9.4
ENV PYTHONUNBUFFERED 1

COPY ../../requirements-prod.txt /code/requirements-prod.txt
WORKDIR /code
RUN pip install -r requirements-prod.txt

COPY ../../ /code

RUN make cython-compile
RUN mkdir /static/ && cd examples && PROD=true python manage.py collectstatic --no-input
