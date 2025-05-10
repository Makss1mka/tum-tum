from fastapi.exceptions import RequestValidationError
from log.loggers import EXCEPTION_HANDLER_LOGGER
from fastapi.responses import JSONResponse
from exceptions import CodeException
from fastapi import Request

async def code_exception_handler(req: Request, ex: CodeException):
    EXCEPTION_HANDLER_LOGGER.exception(f"CODE EXCEPTION: {ex.status_code} | {ex.message}")

    return JSONResponse(
        status_code=ex.status_code,
        content={"error": ex.message},
    )

async def pydantic_validation_exception_handler(req: Request, ex: RequestValidationError):
    EXCEPTION_HANDLER_LOGGER.exception(f"VALIDATION EXCEPTION: {ex.errors} | {ex.__traceback__}")

    return JSONResponse(
        status_code=404,
        content={"error": "Validation failed"},
    )
