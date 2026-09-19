from fastapi import FastAPI
from routes.user_routes import router as user_router

app = FastAPI(title="Spotify Clone API")
app.include_router(user_router, prefix="/api")
# Registrar routers

@app.get("/health")
def health():
    return {"mensaje": "Alive"}
