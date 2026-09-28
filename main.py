from fastapi import FastAPI
from router.data import router as data_router

app = FastAPI(
    title="Weather API",
    description="API for Weather Vision application",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Weather API!"}


app.include_router(data_router)
