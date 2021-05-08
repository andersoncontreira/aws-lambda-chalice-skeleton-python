FROM python:3.8-alpine

MAINTAINER Anderson Contreira <anderson.contreira@gmail.com>

ARG projectName=aws-lambda-chalice-skeleton-python

RUN echo ${projectName}

# copy all files
ADD . /${projectName}

# SQLite support
RUN apk update \
    && apk add sqlite \
    && apk add socat

# gcc requirement for  greenlit and sqlalchemy
RUN apk add build-base

RUN pip install -r ./${projectName}/requirements.txt && \
    pip install -r ./${projectName}/requirements-vendor.txt


EXPOSE 8000

WORKDIR /${projectName}

# CMD
 CMD [ "chalice", "local", "--host", "0.0.0.0" ]
