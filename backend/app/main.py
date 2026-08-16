from fastapi import FastAPI

app = FastAPI(
    title="Mesh API",
    version="0.0.0",
)

@app.get("/")
async def root():
    return {"message": "Mesh API is running"}
