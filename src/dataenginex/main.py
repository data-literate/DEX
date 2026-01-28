from fastapi import FastAPI
import uvicorn

app = FastAPI(title="DataEngineX", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "DataEngineX API", "version": "0.1.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
