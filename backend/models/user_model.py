from database.init import Base
from sqlalchemy import Column, Integer, String

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    username = Column(String, unique=True)

