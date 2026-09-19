from fastapi import FastAPI
from services.user_service import app
app = FastAPI()
@app.get("/")
def read_root():
    return {"mensaje": "Hola mundo"}
