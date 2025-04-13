from pydantic import BaseModel

from models.programa import Programa
from models.lista import Lista


class ListaProgramaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa
        a busca de uma associação entre um programa e uma lista.
    """
    id_lista: int = 1
    id_programa: int = 1
    

class ListaProgramaPostSchema(BaseModel):
    """ Define como uma associação entre um programa (novo ou existente) 
        e uma lista, a ser inserida deve ser representada.
    """
    id_lista: int = 1
    tmdb_id: int = 105
    tipo: str = "movie"
    titulo: str = "De Volta para o Futuro"
    lancamento: str = "1985-07-03"
    url_poster: str = "https://image.tmdb.org/t/p/w342/JoAiVdWmz8XFA9rl43EtjT8ipn.jpg"


class ListaProgramaResponseSchema(BaseModel):
    """ Define como deve ser a resposta após uma requisição
        à associação entre um programa e uma lista.
    """
    mensagem: str
    id_lista: int
    nome_lista: str
    id_programa: int
    tipo: str
    titulo: str


def mesagem_resposta_lista_programa(mensagem: str, lista: Lista, programa: Programa):
    return {
        "mensagem": mensagem,
        "id_lista": lista.id,
        "nome_lista": lista.nome,
        "id_programa": programa.id,
        "tipo": programa.tipo,
        "titulo": programa.titulo
    }