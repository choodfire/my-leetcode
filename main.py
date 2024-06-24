from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index() -> dict:
    return {"Response": "Hello, World!"}
