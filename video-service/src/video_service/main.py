from fastapi import FastAPI
import uvicorn

app = FastAPI()

# app.include_router(router=Router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8082)
