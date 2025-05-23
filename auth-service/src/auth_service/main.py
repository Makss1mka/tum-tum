from config.global_exception_handlers import code_exception_handler, pydantic_validation_exception_handler
from routers.user_creds_router import user_creds_router
from fastapi.exceptions import RequestValidationError
from services.kafka_service import KafkaProducer
from contextlib import asynccontextmanager
from aiokafka import AIOKafkaProducer
from log.setup import setup_logging
from log.loggers import APP_LOGGER
from globals import PORT, HOST
from fastapi import FastAPI
import exceptions
import uvicorn
import os

@asynccontextmanager
async def app_startup(app: FastAPI):
    setup_logging()

    APP_LOGGER.info("Starting server...")

    await KafkaProducer().start()    

    APP_LOGGER.info(f"Server is started on {HOST}:{PORT}")
    yield
    APP_LOGGER.info("Stopping server...")

    await KafkaProducer().stop()

    APP_LOGGER.error("Server stopped.")


app = FastAPI(lifespan=app_startup)

app.add_exception_handler(exceptions.CodeException, code_exception_handler)
#app.add_exception_handler(RequestValidationError, pydantic_validation_exception_handler)

app.include_router(router=user_creds_router)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, log_config=None)