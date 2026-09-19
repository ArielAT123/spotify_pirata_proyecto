from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user_model import Usuario, UsuarioCreate, UsuarioUpdate

async def get_user_by_id(db: AsyncSession, usuario_id: int) -> Usuario | None:
    return await db.get(Usuario, usuario_id)

async def get_user_by_username(db: AsyncSession, username: str) -> Usuario | None:
    result = await db.execute(select(Usuario).where(Usuario.username == username))
    return result.scalar_one_or_none()

async def get_all_users(db: AsyncSession) -> list[Usuario]:
    result = await db.execute(select(Usuario))
    return list(result.scalars().all())

async def create_user(db: AsyncSession, datos: UsuarioCreate) -> Usuario:
    nuevo_usuario = Usuario(**datos.model_dump())
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    return nuevo_usuario

async def update_user(db: AsyncSession, usuario: Usuario, datos: UsuarioUpdate) -> Usuario:
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(usuario, campo, valor)
    await db.commit()
    await db.refresh(usuario)
    return usuario

async def delete_user(db: AsyncSession, usuario: Usuario) -> None:
    await db.delete(usuario)
    await db.commit()