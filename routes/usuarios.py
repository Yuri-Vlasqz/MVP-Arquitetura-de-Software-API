from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError

import logging

from models import Session, Usuario, Lista
from schemas import *
from routes.auth import security_schemes, requires_auth

usuario_tag = Tag(name="Usuários", description="Criação e visualização de usuários")
usuarios_bp = APIBlueprint('usuarios', __name__, url_prefix='/api', abp_tags=[usuario_tag], abp_security=[security_schemes])


@usuarios_bp.get('/usuario', responses={"200": UsuarioResponseSchema, "404": ErrorSchema, "500": ErrorSchema})
@requires_auth
def get_usuario_email(query: UsuarioBuscaEmailSchema):
    """ Busca por um Usuario, a partir do email.
    """
    email = query.email
    
    try:
        session = Session()
        usuario = session.query(Usuario).filter(Usuario.email == email).first()
        if not usuario:
            return {"mensagem": "Usuário nao encontrado."}, 404

        return apresenta_usuario(usuario), 200

    except Exception as e:
        session.rollback()
        logging.error(f"Erro ao buscar usuário: {str(e)}")
        return {"mensagem": str(e)}, 500
    
    finally:
        session.close()


@usuarios_bp.post('/usuario',
                   responses={"201": UsuarioResponseSchema, "409": ErrorSchema, "500": ErrorSchema})
@requires_auth
def post_usuario(form: UsuarioPostSchema):
    """ Cria um usuário a partir do email, com as listas padrão. 
        Listas padrão: "assistidos", "Próximos a ver" e "favoritos".
    """
    usuario = Usuario(email=form.email)
    listas_padrao = [Lista(nome=nome_lista, usuario=usuario) 
                     for nome_lista in ["Favoritos", "Assistidos", "Próximos a ver"]]
    try:
        session = Session()
        session.add(usuario)
        session.add_all(listas_padrao)
        session.commit()
        return mensagem_resposta_usuario("Usuário criado com sucesso.", usuario), 201
    
    except IntegrityError as e:
        logging.warning(f"IntegrityError: {e}")
        return {"mensagem": "Usuário com o mesmo email ja cadastrado."}, 409

    except Exception as e:
        session.rollback()
        logging.error(f"Erro ao criar usuário: {str(e)}")
        return {"mensagem": str(e)}, 500
    
    finally:
        session.close()
        