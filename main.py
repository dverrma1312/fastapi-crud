from fastapi import FastAPI, APIRouter

app = FastAPI(Title="Weather api", description="API for weahterision application", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to Weather API!"}

app.include_router()





