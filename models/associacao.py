from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime

from datetime import datetime

from models.base import Base


# Associação entre listas e programas
lista_programa = Table(
    'lista_programa', Base.metadata,
    Column('lista_id', Integer, ForeignKey('listas.id', ondelete='CASCADE'), primary_key=True),
    Column('programa_id', Integer, ForeignKey('programas.id', ondelete='CASCADE'), primary_key=True),
    Column('data_associacao', DateTime, default=datetime.now())
)
