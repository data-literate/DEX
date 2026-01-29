import uvicorn
from fastapi import FastAPI

app = FastAPI(title="DataEngineX", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "DataEngineX API", "version": "0.1.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/ready")
def readiness_check():
    return {"status": "ready"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
