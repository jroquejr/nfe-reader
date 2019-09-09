FROM python:3.7-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache --virtual .build-deps gcc musl-dev cython 

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH $PYTHONPATH:/usr/src/app

COPY Pipfile Pipfile.lock /usr/src/app/

RUN pip install pipenv \
    && pipenv install --system --deploy


RUN apk del .build-deps gcc musl-dev

COPY . /usr/src/app