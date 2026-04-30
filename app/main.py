from fastapi import FastAPI

app = FastAPI(title="Online Exchange System API")

@app.get("/")
def root():
    return {"message": "Online Exchange System Running"}
