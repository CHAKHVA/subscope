import os

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI(title="Subscope API")


@app.get("/")
async def read_root():
    return {"message": "Welcome to Subscope API!"}


@app.get("/health")
async def health_check():
    # You can add a DB check here later
    return {"status": "ok", "db_host": os.getenv("POSTGRES_HOST")}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 80)),
    )
