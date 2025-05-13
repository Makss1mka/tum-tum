from config.global_exception_handlers import code_exception_handler, pydantic_validation_exception_handler
from routers.user_creds_router import user_creds_router
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from log.setup import setup_logging
from log.loggers import APP_LOGGER
from globals import PORT, HOST
from fastapi import FastAPI
import exceptions
import uvicorn

@asynccontextmanager
async def app_startup(app: FastAPI):
    setup_logging()
    APP_LOGGER.info(f"Server is started on {HOST}:{PORT}")
    yield
    APP_LOGGER.error("Server shutdown...")


app = FastAPI(lifespan=app_startup)

app.add_exception_handler(exceptions.CodeException, code_exception_handler)
#app.add_exception_handler(RequestValidationError, pydantic_validation_exception_handler)

app.include_router(router=user_creds_router) # , prefix='/api/v1'

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, log_config=None)