from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from datetime import datetime

from models.associacao import lista_programa
from models.base import Base


class Lista(Base):
    __tablename__ = 'listas'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)

    # Deleção de usuário cascateia para listas. | coluna usuario_id indexada para otimizar consultas
    usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False, index=True)
    data_insercao = Column(DateTime, default=datetime.now())
    
    # Relação N:1 - listas -> usuário
    usuario = relationship("Usuario", back_populates="listas")
    
    # Relação N:N - listas -> programas
    programas = relationship("Programa", secondary=lista_programa, back_populates="listas", passive_deletes=True)

    # Definição de unicidade para NÃO permitir listas de mesmo nome e de um mesmo usuário
    __table_args__ = (UniqueConstraint('nome', 'usuario_id', name='_nome_lista_unica'),) 
    # OBS: table_args is supposed to be a tuple !!!
    # A trailing comma is needed to distinguish a (single-item,) tuple constructor from an (expression).
