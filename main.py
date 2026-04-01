from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/learn")
async def learn_fastapi():
    return {"msg":"我正在学习FastAPI！"}