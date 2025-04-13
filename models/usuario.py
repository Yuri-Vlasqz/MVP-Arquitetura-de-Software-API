from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime

from models.base import Base


class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(128), unique=True, nullable=False)
    data_insercao = Column(DateTime, default=datetime.now())
    
    # Relação 1:N - usuario -> listas
    listas = relationship("Lista", back_populates="usuario", cascade="all, delete, delete-orphan")
    # Ao deletar o usuário, as listas associadas são removidas.
    