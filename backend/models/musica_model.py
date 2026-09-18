from sqlalchemy import Column, Integer, String
from database.init import Base

class Musica(Base):
    __tablename__ = "musica"
    id_musica = Column(Integer, primary_key=True, index=True)
    nombre_musica = Column(String, index=True)
    foto_preview = Column(String, unique=True)
    url= Column(String, unique=True)