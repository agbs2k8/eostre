# API for Admin Service
This is an async python API built around quart.

## Table of contents

- Requirements
- Installation
- Configuration and Development
- Deployment
- FAQ
- Maintainers

## Requirements
1. Pipenv
2. Python 3.13.3
3. Refer Pipfile

## Installation

### Setup Python Environment
- `pipenv install`

## Configuration and Development

### Setup

- Make configurations and set environment variables as/if needed in `config.py`

### Start API
- Setup 
    
    `source ../export_locals.sh` 

- Standard
    
    `export QUART_APP=main.py && quart run`

- Development

    `export QUART_APP=main.py && quart run  --debug`

- Custom Host

    `export QUART_APP=main.py && quart run  --host=0.0.0.0`

### Run Tests 
- Standard 

    `python -m pytest -v`

- With verbose logs

    `python -m pytest -v -s`

- With hidden warnings

    `python -m pytest -v --disable-warnings`

- Get tests coverage (you may need to run `pip install pytest-cov` first)

    `python -m pytest --cov .`


## Deployment
1. Build & run local docker image #TODO - FIX MONGOIMAGE STUFF

    `docker build -t agbs2k8/apiserv:latest .`
    `docker run --env-file .env --add-host=mongoservice:127.0.0.1 -p 8080:8080 agbs2k8/apiserv:latest`

2. If everything looks good, push it to Docker Hub so that k3d can pull it

    `docker push agbs2k8/apiserv:latest`

### k3s (k3d locally) 
1. Ensure that k3s can import the image

    `k3d image import apiserv:latest -c <your-cluster-name>`

2. Insert the secrets into the cluster
    
    `kubectl create secret generic apiserv-secrets --from-env-file=.env`

3. Install the image using helm

    `helm install apiserv ./ --values values.yaml`

4. Upgrade an existing k3s image

    `helm upgrade apiserv ./ --values values.yaml`

3. Connect to the service

   `http://apiserv.local/api/v1/liveness`


## FAQ
**Q: How to test the application locally?** 

**A:** 
1. Follow the steps in [Installation](#installation) and [Configuration and Development](#configuration-and-development) sections.
2. Start the application using [Start API](#start-api) section.
3. Use the Postman to test the application.
+
**Q: How to get the API collection importable JSON for Postman?** 

**A:** 
    Get the API collection importable JSON from [here](../)



## Maintainers

- AJ Wilson - [AJ](https://github.com/agbs2k8)