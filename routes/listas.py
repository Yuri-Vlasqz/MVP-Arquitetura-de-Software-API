from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError

import logging

from models import Session, Lista, Usuario
from schemas import *
from routes.auth import security_schemes, requires_auth

lista_tag = Tag(name="Listas", description="Criação, atualização e remoção de listas")
listas_bp = APIBlueprint('listas', __name__, url_prefix='/api', abp_tags=[lista_tag], abp_security=[security_schemes])


@listas_bp.post('/lista', 
          responses={"201": ListaResponseSchema, "404": ErrorSchema, "409": ErrorSchema, "500": ErrorSchema})
@requires_auth
def post_lista(form: ListaPostSchema):
    """ Adiciona uma nova lista atrelada a um usuário, 
        a partir do id do usuário e nome da lista.
    """
    nome_lista = form.nome
    id_usuario = form.usuario_id

    try:
        session = Session()
        usuario = session.get(entity=Usuario, ident=id_usuario)
        if not usuario:
            return {"mensagem": "Usuário não encontrado."}, 404

        lista = Lista(nome=nome_lista, usuario=usuario)
        session.add(lista)
        session.commit()
        return mensagem_resposta_lista("Lista criada com sucesso.", lista), 201
    
    except IntegrityError as e:
        logging.warning(f"IntegrityError: {e}")
        return {"mensagem": "Lista com o mesmo nome e usuário ja cadastrada."}, 409
    
    except Exception as e:
        session.rollback()
        logging.error(f"Erro ao criar lista: {str(e)}")
        return {"mensagem": str(e)}, 500
    
    finally:
        session.close()


@listas_bp.put('/lista', 
         responses={"200": ListaResponseSchema, "404": ErrorSchema, "409": ErrorSchema, "500": ErrorSchema})
@requires_auth
def put_lista(form: ListaPutSchema):
    """ Atualiza informações de uma lista, a partir do id.	
    """
    id_lista = form.id
    novo_nome = form.novo_nome

    try:
        session = Session()
        lista = session.get(entity=Lista, ident=id_lista)
        if not lista:
            return {"mensagem": "Lista não encontrada."}, 404

        if novo_nome != lista.nome:
            lista.nome = novo_nome
            session.commit()
        return mensagem_resposta_lista("Lista atualizada com sucesso.", lista), 200

    except IntegrityError as e:
        logging.warning(f"IntegrityError: {e}")
        return {"mensagem": "Lista com o mesmo nome e usuário ja cadastrada."}, 409

    except Exception as e:
        session.rollback()
        logging.error(f"Erro ao atualizar lista: {str(e)}")
        return {"mensagem": str(e)}, 500
    
    finally:
        session.close()


@listas_bp.delete('/lista', 
            responses={"200": ListaResponseSchema, "404": ErrorSchema, "500": ErrorSchema})
@requires_auth
def del_lista(query: ListaBuscaIdSchema):
    """ Deleta uma lista, a partir do id.
    """
    id_lista = query.id

    try:
        session = Session()
        lista = session.get(entity=Lista, ident=id_lista)
        if not lista:
            return {"mensagem": "Lista nao encontrada."}, 404

        session.delete(lista)
        session.commit()
        return mensagem_resposta_lista("Lista deletada com sucesso.", lista), 200

    except Exception as e:
        session.rollback()
        logging.error(f"Erro ao deletar lista: {str(e)}")
        return {"mensagem": str(e)}, 500
    
    finally:
        session.close()
