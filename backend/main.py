from fastapi import FastAPI

app = FastAPI(
    title="Energy Report Assistant",
    description="AI-powered platform for energy and operational report analysis",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "project": "Energy Report Assistant",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }