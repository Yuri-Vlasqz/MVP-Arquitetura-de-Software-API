from flask import redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag

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
info = Info(title="Teste API - Todos a ver", version="1.7.0")
app = OpenAPI(__name__, info=info, security_schemes=security_schemes)
CORS(app)  # Desenvolvimento local

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")


@app.get('/', tags=[home_tag])
def home():
    """ Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


app.register_api(tmdb_bp)            # Chamadas ao TMDB para obtenção de informações de programas
app.register_api(usuarios_bp)        # Adição, visualização, atualização e remoção de usuários
app.register_api(listas_bp)          # Adição, atualização e remoção de listas
app.register_api(programa_lista_bp)  # Adição e remoção de programas de uma lista


# === Melhorias ===
# TODO: indicar <path> nas rotas de query de elemento unico?

# TODO: migrar para sqlalchemy 2.0 
# -> https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#migrating-an-existing-mapping