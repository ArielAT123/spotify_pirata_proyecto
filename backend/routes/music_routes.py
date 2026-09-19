from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.init import get_db
from models.musica_model import MusicaCreate, MusicaUpdate, MusicaResponse
from services import music_services

router = APIRouter(prefix="/musica", tags=["Musica"])

@router.get("", response_model=list[MusicaResponse])
async def listar_musica(db: AsyncSession = Depends(get_db)):
    return await music_services.get_all_music(db)

@router.get("/{id_musica}", response_model=MusicaResponse)
async def obtener_musica(id_musica: int, db: AsyncSession = Depends(get_db)):
    musica = await music_services.get_musica_by_id(db, id_musica)
    if not musica:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Musica no encontrada")
    return musica

@router.post("", response_model=MusicaResponse, status_code=status.HTTP_201_CREATED)
async def crear_musica(datos: MusicaCreate, db: AsyncSession = Depends(get_db)):
    musica_existente = await music_services.get_musica_by_name(db, datos.nombre_musica)
    if musica_existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Esta musica ya existe")
    return await music_services.create_music(db, datos)

@router.put("/{id_musica}", response_model=MusicaResponse)
async def actualizar_musica(id_musica: int, datos: MusicaUpdate, db: AsyncSession = Depends(get_db)):
    musica = await music_services.get_musica_by_id(db, id_musica)
    if not musica:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Musica no encontrada")
    
    if datos.nombre_musica and datos.nombre_musica != musica.nombre_musica:
        musica_existente = await music_services.get_musica_by_name(db, datos.nombre_musica)
        if musica_existente:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El nombre de la musica ya esta en uso")

    return await music_services.update_music(db, musica, datos)

@router.delete("/{id_musica}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_musica(id_musica: int, db: AsyncSession = Depends(get_db)):
    musica = await music_services.get_musica_by_id(db, id_musica)
    if not musica:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Musica no encontrada")
    await music_services.delete_music(db, musica)
