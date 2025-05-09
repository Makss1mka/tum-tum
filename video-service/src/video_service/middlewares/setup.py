from main import app
from auth import auth
from fastapi import Request

@app.middleware("/")
async def main_middleware(req: Request, call_next):
    auth(req)

    resp = await call_next(req)

    return resp


