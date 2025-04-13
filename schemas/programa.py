from pydantic import BaseModel

from datetime import date

from models.programa import Programa


class ProgramaViewSchema(BaseModel):
    """ Define como um programa sera retornado.
    """
    id: int
    tmdb_id: int
    tipo: str
    titulo: str
    lancamento: date
    url_poster: str


def apresenta_programa(programa: Programa):
    """ Retorna uma representação da programa seguindo o schema definido em
        ProgramaViewSchema.
    """
    return {
        "id": programa.id,
        "tmdb_id": programa.tmdb_id,
        "tipo": programa.tipo,
        "titulo": programa.titulo,
        "lancamento": programa.lancamento,
        "url_poster": programa.url_poster
    }