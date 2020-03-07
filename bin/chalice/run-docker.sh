#!/bin/bash

# encontra a porta e remove o nome da variable
PORT=$(grep PORT .env | sed -e "s/PORT=//g" | xargs)

if [ -z "$PORT" ]
then
  PORT=8000
fi

# echo $PORT
docker run -p $PORT:8000 project-name-chalice:latest