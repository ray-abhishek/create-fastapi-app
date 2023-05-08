import time
import logging.config

import sentry_sdk
import structlog
import strawberry
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration

from app import settings
from app.logger import sentry_processor
from strawberry.fastapi import GraphQLRouter
from app.core import Query, Mutation


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

  
app = FastAPI()


sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    request_bodies="medium",
    environment=settings.ENV,
    integrations=[
        StarletteIntegration(transaction_style="endpoint"),
        FastApiIntegration(transaction_style="endpoint"),
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def setup_logging() -> None:
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            *settings.shared_processors,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            sentry_processor,
            structlog.processors.JSONRenderer(sort_keys=True),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True
    )
    logging.config.dictConfig(settings.LOGGING)



@app.on_event("startup")
async def startup_event() -> None:
    setup_logging()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    This middleware adds a header to the response with the time it took to process the request.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# healthcheck endpoint
@app.get("/health-check")
def healthcheck():
    """
    Healthcheck endpoint that can be used a liveness probe.
    """
    return {"message": "healthy"}


app.include_router(graphql_app, prefix="/graphql")
