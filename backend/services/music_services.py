from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.musica_model import Musica, MusicaCreate, MusicaUpdate

async def get_musica_by_id(db: AsyncSession, id_musica:int) -> Musica | None:
    return await db.get(Musica, id_musica)

async def get_musica_by_name(db: AsyncSession, nombre_musica:str) -> Musica | None:
    result = await db.execute(select(Musica).where(Musica.nombre_musica == nombre_musica))
    return result.scalar_one_or_none()

async def get_all_music(db: AsyncSession) -> list[Musica]:
    result = await db.execute(select(Musica))
    if not result:
        return []
    return list(result.scalars().all())

async def create_music(db: AsyncSession, datos: MusicaCreate) -> Musica:
    nueva_musica = Musica(**datos.model_dump())
    db.add(nueva_musica)
    await db.commit()
    await db.refresh(nueva_musica)
    return nueva_musica

async def update_music(db: AsyncSession, musica: Musica, datos: MusicaUpdate) -> Musica:
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(musica, campo, valor)
    await db.commit()
    await db.refresh(musica)
    return musica

async def delete_music(db: AsyncSession, musica: Musica) -> None:
    await db.delete(musica)
    await db.commit()   