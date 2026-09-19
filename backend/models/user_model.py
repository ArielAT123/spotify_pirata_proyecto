from database.init import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, ConfigDict

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    username = Column(String, unique=True)


# Lo que el cliente envía para crear un usuario
class UsuarioCreate(BaseModel):
    nombre: str
    username: str

# Lo que el cliente puede enviar para actualizar (todo opcional)
class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    username: str | None = None

# Lo que la API devuelve al cliente
class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    username: str

    model_config = ConfigDict(from_attributes=True)  # permite leer desde objetos SQLAlchemy