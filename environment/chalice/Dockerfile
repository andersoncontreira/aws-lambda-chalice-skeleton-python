FROM python:3.8

MAINTAINER Anderson Contreira <anderson.contreira@gmail.com>

ARG projectName=project-name-chalice

RUN echo ${projectName}

# copy all files
ADD . /${projectName}

RUN pip install -r ./${projectName}/requirements-chalice.txt && \
    pip install -r ./${projectName}/requirements.txt

EXPOSE 8000

WORKDIR /${projectName}

# OK - ENTRYPOINT
#ENTRYPOINT [ "chalice", "local", "--host", "0.0.0.0" ]

# CMD
CMD [ "chalice", "local", "--host", "0.0.0.0" ]


