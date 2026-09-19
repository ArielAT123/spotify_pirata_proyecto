from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.init import get_db
from models.user_model import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from services import user_service

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# ---------- GET (todos) ----------
@router.get("", response_model=list[UsuarioResponse])
async def listar_usuarios(db: AsyncSession = Depends(get_db)):
    return await user_service.get_all_users(db)

# ---------- GET (uno solo) ----------
@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    usuario = await user_service.get_user_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario

# ---------- POST (crear) ----------
@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(datos: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    usuario_existente = await user_service.get_user_by_username(db, datos.username)
    if usuario_existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este usuario ya existe")
    return await user_service.create_user(db, datos)

# ---------- PUT (actualizar) ----------
@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate, db: AsyncSession = Depends(get_db)):
    usuario = await user_service.get_user_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    if datos.username and datos.username != usuario.username:
        usuario_existente = await user_service.get_user_by_username(db, datos.username)
        if usuario_existente:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El username ya está en uso")

    return await user_service.update_user(db, usuario, datos)

# ---------- DELETE (eliminar) ----------
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    usuario = await user_service.get_user_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    await user_service.delete_user(db, usuario)
