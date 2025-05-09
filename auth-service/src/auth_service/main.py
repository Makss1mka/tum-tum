from log.setup import setup_logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from globals import PORT, HOST
from log.loggers import APP_LOGGER
import uvicorn
import exceptions
from config.global_exception_handlers import code_exception_handler

@asynccontextmanager
async def app_startup(app: FastAPI):
    setup_logging()
    APP_LOGGER.info(f"Server is started on {HOST}:{PORT}")
    yield
    APP_LOGGER.error("Server shutdown...")


app = FastAPI(lifespan=app_startup)

app.add_exception_handler(exceptions.CodeException, code_exception_handler)

# app.include_router(router=Router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, log_config=None)