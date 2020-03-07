# Aws Lambda Chalice Skeleton for python 
Skeleton to create microservices using Chalice and Lambda.

## Release notes 

In this section contains the release notes of the project.

> Version 1.0.0

 * First version of the project;

All the changes must be tracked in [CHANGELOG.md](CHANGELOG.md)

## Features
 * Basic RESTful structure;;
 * Docker to development environment;
 * Binaries commands to automatize some actions;
 * Environment variables support;
 * Unit and Functional tests structure;
 

## Installing

### Installing in the virtual environment
execute the follow command:
```
./bin/chalice/venv.sh
```

### Installing without a virtual environment
#### Installing public dependencies
execute the follow command:
```
./bin/chalice/install.sh
```
#### Installing private dependencies only
execute the follow command:
```
./bin/chalice/install-vendor.sh
```

## Building
execute the follow command:
```
./bin/chalice/build.sh
```
## Running locally
execute the follow command:
```
./bin/chalice/run-local.sh
```
## Working with Docker
If you are working with `Docker` follow the further steps.

### Installing vendor modules
execute the follow command:
```
./bin/chalice/install-vendor.sh
```

### Building Docker
execute the follow command:
```
./bin/chalice/build.sh
```

### Running Docker
execute the follow command:
```
./bin/chalice/run-docker.sh
```

### Running Docker Compose
execute the follow command:
```
./bin/chalice/run-docker-compose.sh
```
Or:
```
./bin/chalice/run-docker-compose.sh -d --build
```

## Getting started

### Project setup
You need to create a `.env` to work locally, you can copy the file `.env.example`.

File example:
```
APP_ENV=development
APP_HOST=localhost
PORT=8000
HTTPS=False
DEBUG=False
```

## Running tests

To run the unit tests of the project you can execute the follow command:

### Installing tests dependencies
execute the follow command:
```
./bin/install-tests.sh
```
### Running tests scenarios 

All tests:
``` 
./bin/test.sh 
```

Unit tests:
``` 
./bin/unit-tests.sh 
```

Functional tests:
``` 
./bin/functional-tests.sh 
```
