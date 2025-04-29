from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError

import logging

from models import Session, Lista, Programa
from schemas import *
from routes.auth import security_schemes, requires_auth

programa_lista_tag = Tag(name="Programas", description="Adição e remoção de programas de uma lista")
programa_lista_bp = APIBlueprint('programas', __name__, url_prefix='/api', abp_tags=[programa_lista_tag], abp_security=[security_schemes])


@programa_lista_bp.post('/programa-lista', 
          responses={"201": ListaProgramaResponseSchema, "404": ErrorSchema, "409": ErrorSchema, "500": ErrorSchema})
@requires_auth
def post_programa_de_lista(form: ListaProgramaPostSchema):
    """ Adiciona uma associação entre um programa e uma lista, a partir de seus id's.
        OBS: Cria um programa se ele não existir.
    """
    id_lista = form.id_lista
    tmdb_id  = form.tmdb_id
    tipo     = form.tipo

    try:
        session = Session()
        lista = session.get(entity=Lista, ident=id_lista)
        if not lista:
            return {"mensagem": "Lista não encontrada."}, 404

        programa = session.query(Programa).filter_by(tmdb_id=tmdb_id, tipo=tipo).one_or_none()
        if programa in lista.programas:
            logging.warning("Programa ja associado a lista.")
            return {"mensagem": "Programa já associado a lista."}, 409
        
        msg_extra = ""
        
        if not programa:
            # Caso o programa não exista, ele é criado.
            titulo      = form.titulo
            lancamento  = form.lancamento
            url_poster  = form.url_poster
            programa = Programa(tmdb_id=tmdb_id, tipo=tipo, titulo=titulo, lancamento=lancamento, url_poster=url_poster)
            session.add(programa)
            msg_extra = "criado e "

        lista.programas.append(programa)
        session.commit()
        return mesagem_resposta_lista_programa(f"Programa {msg_extra}associado a lista com sucesso.", lista, programa), 201
    
    except IntegrityError as e:
        logging.warning(f"IntegrityError: {e}")
        return {"mensagem": "Programa de mesmo tmdb_id e tipo já cadastrado."}, 409

    except Exception as e:
        session.rollback()
        logging.error(f"Erro ao associar programa a lista: {str(e)}")
        return {"mensagem": str(e)}, 500

    finally:
        session.close()


@programa_lista_bp.delete('/programa-lista',
            responses={"200": ListaProgramaResponseSchema, "404": ErrorSchema, "500": ErrorSchema})
@requires_auth
def del_programa_de_lista(query: ListaProgramaBuscaSchema):
    """Remove uma associação entre um programa e uma lista, a partir de seus id's.
    """
    id_lista    = query.id_lista
    id_programa = query.id_programa

    try:
        session = Session()
        lista = session.get(entity=Lista, ident=id_lista)
        programa = session.get(entity=Programa, ident=id_programa)
        if not lista:
            logging.warning("Lista nao encontrada.")
            return {"mensagem": "Lista não encontrada."}, 404

        if not programa:
            logging.warning("Programa nao encontrado.")
            return {"mensagem": "Programa não encontrado."}, 404

        if programa not in lista.programas:
            logging.warning("Associação de programa e lista nao encontrada.")
            return {"mensagem": "Associação de programa e lista não encontrada."}, 404

        lista.programas.remove(programa)
        session.commit()
        return mesagem_resposta_lista_programa("Programa removido da lista com sucesso.", lista, programa), 200

    except Exception as e:
        session.rollback()
        logging.error(f"Erro ao remover programa da lista: {str(e)}")
        return {"mensagem": str(e)}, 500

    finally:
        session.close()
