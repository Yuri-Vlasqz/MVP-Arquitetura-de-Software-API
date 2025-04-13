from pydantic import BaseModel

from datetime import datetime
from typing import Optional, List

from models.usuario import Usuario
from schemas.lista import ListaViewSchema, apresenta_lista


class UsuarioBuscaEmailSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca de usuário, por email.
    """
    email: str = "email@teste.com"


class UsuarioPostSchema(BaseModel):
    """ Define como um novo usuário a ser criado deve ser representado.
    """
    email: str = "email@teste.com"


class UsuarioResponseSchema(BaseModel):
    """ Define como deve ser a resposta após uma requisição
        do tipo POST, PUT ou DELETE ao usuário.
    """
    mensagem: str
    id: int
    email: str


def mensagem_resposta_usuario(mensagem: str, usuario: Usuario):
    """ Retorna uma representação da mensagem de resposta de requisição ao usuario.
    """
    return {
        "mensagem": mensagem,
        "id": usuario.id,
        "email": usuario.email
    }


class UsuarioViewSchema(BaseModel):
    """  Define como um usuario será retornado: usuario + listas.
    """
    id: int
    nome: str
    email: str
    listas: List[ListaViewSchema]
    data_insercao: datetime


def apresenta_usuario(usuario: Usuario):
    """ Retorna uma representação do usuario seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": usuario.id,
        "email": usuario.email,
        "listas": [apresenta_lista(lis) for lis in usuario.listas],
        "data_insercao": usuario.data_insercao
    }
