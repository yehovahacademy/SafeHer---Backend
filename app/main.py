
from fastapi import FastAPI

app = FastAPI(
    title="Mumbai SafeRoute API",
    description="A prototype for route comparison and safety indicators in Mumbai.",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "message": "Mumbai SafeRoute API is running",
        "city": "Mumbai",
        "status": "development",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
