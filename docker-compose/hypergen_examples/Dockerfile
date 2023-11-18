FROM python:3.9.4
ENV PYTHONUNBUFFERED 1
RUN echo bump
COPY docker-compose/hypergen_examples/entrypoint.sh /entrypoint.sh

COPY ../../requirements-prod.txt /code/requirements-prod.txt
WORKDIR /code
RUN pip install -r requirements-prod.txt

COPY ../../examples /code/examples
COPY ../../src /code/src
COPY ../../Makefile /code/Makefile
COPY ../../setup.cfg /code/setup.cfg
COPY ../../.github/workflows/pytest.yml /code/.github/workflows/pytest.yml

RUN make cython-compile
RUN mkdir /static/
