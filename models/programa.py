from sqlalchemy import Column, Integer, String, DateTime, Date, UniqueConstraint
from sqlalchemy.orm import relationship

from datetime import datetime

from models.associacao import lista_programa
from models.base import Base


class Programa(Base):
    __tablename__ = 'programas'
    
    id = Column(Integer, primary_key=True)
    tmdb_id = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)
    titulo = Column(String, nullable=False)
    lancamento = Column(Date, nullable=False)
    url_poster = Column(String)
    
    # Relação - programas N:N com listas
    listas = relationship("Lista", secondary=lista_programa, back_populates="programas", passive_deletes=True)
    # Ao deletar o programa, as lista_programa's associadas são removidas.

    # Definição de unicidade para NÃO permitir programas duplicados
    __table_args__ = (UniqueConstraint('tmdb_id', 'tipo', name='_id_tmdb_unico'),) 
    # OBS: table_args is supposed to be a tuple !!!
    # A trailing comma is needed to distinguish a (single-item,) tuple constructor from an (expression).

    def __init__(self, tmdb_id: int, tipo: str, titulo: str, lancamento: str, url_poster: str | None = None):
        """ Cria uma instância da classe Programa. """
        self.tmdb_id = tmdb_id
        self.tipo = tipo
        self.titulo = titulo
        self.lancamento = datetime.strptime(lancamento, '%Y-%m-%d').date()
        self.url_poster = url_poster
