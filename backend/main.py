from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="AI Interview Platform API",
    description="Backend APIs for AI Interview Platform",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "AI Interview Platform Backend Running Successfully"
    }