from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database.init import Base
detalle_playlist = Table(
    "det_playlist",
    Base.metadata,
    Column("id_playlist", Integer, ForeignKey("playlist.id_playlist"), primary_key=True),
    Column("id_musica", Integer, ForeignKey("musica.id_musica"), primary_key=True),
)

class Playlist(Base):
    __tablename__ = "playlist"
    id_playlist = Column(Integer, primary_key=True, index=True)
    nombre= Column(String, index=True)
    user_id = Column(Integer, ForeignKey("usuario.id"))
    det_playlist = relationship("Musica", secondary=detalle_playlist)



