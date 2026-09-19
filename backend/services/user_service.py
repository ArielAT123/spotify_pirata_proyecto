from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.user_models import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioResponse


app = FastAPI()

# ---------- GET (uno solo) ----------
@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    usuario = await db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# ---------- POST (crear) ----------
@app.post("/usuarios", response_model=UsuarioResponse, status_code=201)
async def crear_usuario(datos: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    nuevo_usuario = Usuario(**datos.model_dump())
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    return nuevo_usuario

# ---------- PUT (actualizar) ----------
@app.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate, db: AsyncSession = Depends(get_db)):
    usuario = await db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # solo actualiza los campos que vinieron en la petición
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(usuario, campo, valor)

    await db.commit()
    await db.refresh(usuario)
    return usuario

# ---------- DELETE ----------
@app.delete("/usuarios/{usuario_id}", status_code=204)
async def eliminar_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    usuario = await db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    await db.delete(usuario)
    await db.commit()