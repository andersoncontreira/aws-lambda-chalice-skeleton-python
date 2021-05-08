FROM node:12-alpine

MAINTAINER Anderson Contreira <anderson.contreira@gmail.com>

ARG projectName=api-mock

RUN echo ${projectName}

WORKDIR /app

#RUN npm init
RUN npm install -g json-server

COPY ./samples /app/samples

EXPOSE 3000

# CMD
# ENTRYPOINT ["json-server", "--host", "0.0.0.0"]
CMD [ "json-server","--host", "0.0.0.0","--watch","/app/samples/api-mock/db.json", "--routes","/app/samples/api-mock/routes.json","--id","skuFiltered" ]
