# create-fastapi-app

## This repo provides a project template of a FastAPI application using Strawberry for GraphQL API

Following things have been taken care of : 
1. Dockerizing the application.
2. Building & pushing the image to AWS ECR via Github Action.
3. Setting up logging & sentry.
4. Basic structure of codebase
5. Basic requirements such as : FastAPI, Pytest, Strawberry, structlog

## Usage : 

1. Clone the repo to local.
2. Create a virtualenv
3. Install the requirements
4. Start server `uvicorn app.main:app --reload`
