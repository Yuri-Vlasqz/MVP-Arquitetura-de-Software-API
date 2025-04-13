from pydantic import BaseModel

from datetime import datetime
from typing import List

from models.lista import Lista
from schemas.programa import ProgramaViewSchema, apresenta_programa


class ListaBuscaIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa
        a busca de uma lista em um usuário, pelos id's de cada.
    """
    id: int = 1


class ListaPostSchema(BaseModel):
    """ Define como um nova lista a ser inserida deve ser representada.
    """
    usuario_id: int = 1
    nome: str = "Lista teste"


class ListaPutSchema(BaseModel):
    """ Define como uma lista a ser editada deve ser representada.
    """
    id: int = 1
    novo_nome: str = "Lista editada"


class ListaResponseSchema(BaseModel):
    """ Define como deve ser a resposta após uma requisição
        do tipo POST, PUT ou DELETE à lista.
    """
    mensagem: str
    id: int
    nome: str
    usuario_id: int


def mensagem_resposta_lista(mensagem: str, lista: Lista):
    """ Retorna uma representação da mensagem de resposta de requisição à lista.
    """
    return {
        "mensagem": mensagem,
        "id": lista.id,
        "nome": lista.nome,
        "usuario_id": lista.usuario_id,
    }


class ListaViewSchema(BaseModel):
    """ Define como uma lista será retornada: lista + programas.
    """
    id: int
    nome: str
    usuario_id: int
    programas: List[ProgramaViewSchema]
    data_insercao: datetime


def apresenta_lista(lista: Lista):
    """ Retorna uma representação da lista seguindo o schema definido em
        ListaViewSchema.
    """
    return {
        "id": lista.id,
        "nome": lista.nome,
        "usuario_id": lista.usuario_id,
        "programas": [apresenta_programa(prog) for prog in lista.programas],
        "data_insercao": lista.data_insercao
    }