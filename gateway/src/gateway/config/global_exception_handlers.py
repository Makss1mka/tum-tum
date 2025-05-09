from log.loggers import EXCEPTION_HANDLER_LOGGER
from exceptions import CodeException
from fastapi.responses import JSONResponse
from fastapi import Request

async def code_exception_handler(req: Request, ex: CodeException):
    EXCEPTION_HANDLER_LOGGER.exception(f"CODE EXCEPTION: {ex.status_code} | {ex.message}")

    return JSONResponse(
        status_code=ex.status_code,
        content={"error": ex.message},
    )
