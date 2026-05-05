from fastapi import FastAPI

app = FastAPI(title="OpenSnep API")

@app.get("/")
def root():
    return {"message: Welcome to OpenSnep"}