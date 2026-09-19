from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.music_routes import router as music_router

app = FastAPI(title="Spotify Clone API")
app.include_router(user_router, prefix="/api")
app.include_router(music_router, prefix="/api")

@app.get("/health")
def health():
    return {"mensaje": "Alive"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8100, reload=True)
