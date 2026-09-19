from sqlalchemy import Column, Integer, String
from database.init import Base
from pydantic import BaseModel, ConfigDict

class Musica(Base):
    __tablename__ = "musica"
    id_musica = Column(Integer, primary_key=True, index=True)
    nombre_musica = Column(String, index=True)
    foto_preview = Column(String, unique=True)
    url= Column(String, unique=True)


class MusicaCreate(BaseModel):
    nombre_musica: str
    foto_preview: str
    url: str

class MusicaUpdate(BaseModel):
    nombre_musica: str | None = None
    foto_preview: str | None = None
    url: str | None = None

class MusicaResponse(BaseModel):
    id_musica: int
    nombre_musica: str
    foto_preview: str
    url: str

    model_config = ConfigDict(from_attributes=True)

    