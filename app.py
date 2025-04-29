from flask import redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag

import logging

from routes.auth import security_schemes
from routes.listas import listas_bp
from routes.programa_lista import programa_lista_bp
from routes.tmdb import tmdb_bp
from routes.usuarios import usuarios_bp


# Versões
# - 1.0.0 -> Reaproveitamento do MVP de Fullstack Básico.
# - 1.5.0 -> Adaptacão para MVP de Arquitetura de Software.
# - 1.6.0 -> Implementação de APIBlueprint e mudança de estrutura do projeto.
# - 1.7.0 -> Implementação de autenticação com Auth0 para rotas protegidas.
info = Info(title="Teste API - Tudo a ver", version="2.0.0")
app = OpenAPI(__name__, info=info, security_schemes=security_schemes)
CORS(app)  # Desenvolvimento local


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")


@app.get('/', tags=[home_tag])
def home():
    """ Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


app.register_api(tmdb_bp)            # Chamadas ao TMDB para obtenção de informações de programas
app.register_api(usuarios_bp)        # Adição e visualização de usuários
app.register_api(listas_bp)          # Adição, atualização e remoção de listas
app.register_api(programa_lista_bp)  # Adição e remoção de programas de uma lista


if __name__ == '__main__':
    # Teste rápido de debug: python app.py
    app.run(host='0.0.0.0', port=5000, debug=True)


# === Melhorias ===
# TODO: indicar <path> nas rotas de query de elemento unico?

# TODO: migrar para sqlalchemy 2.0 
# -> https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#migrating-an-existing-mapping