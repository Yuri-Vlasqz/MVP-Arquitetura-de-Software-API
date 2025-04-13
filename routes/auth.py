import requests
from dotenv import load_dotenv
from flask import jsonify, request
from flask_openapi3 import APIBlueprint, Tag
from jose import jwt

import json, os
from functools import wraps
from urllib.request import urlopen


auth_tag = Tag(name="Auth0 - API externa", description="Requisição de token ao Auth0")
auth_bp = APIBlueprint('auth', __name__, url_prefix='/api', abp_tags=[auth_tag])

# Variáveis .env do Auth0
load_dotenv()
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_API_AUDIENCE = os.getenv('AUTH0_API_AUDIENCE')
ALGORITHMS = ['RS256']

# security_schemes -> https://luolingchun.github.io/flask-openapi3/v3.x/Usage/Specification/#security_schemes
token = {
  "type": "http",
  "scheme": "bearer",
  "bearerFormat": "JWT",
  "description": "Digite o header de autorização do tipo `Bearer <token>` adquirido pelo Auth0",
}
security_schemes = {"Token-Auth0": token}


# Função auxiliar para obter a chave pública do Auth0
def get_auth0_public_key():
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    return jwks


# Decorator para verificar token JWT
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        # Verificar se o header de autorização está presente
        if not auth_header:
            return jsonify({'message': 'Token de autorização ausente'}), 401
        
        # Verificar formato do token Bearer
        if not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Formato de token inválido. Use "Bearer <token>"'}), 401
        
        # Extrair o token
        token = auth_header.split(' ')[1]
        
        try:
            # Obter as chaves públicas do Auth0
            jwks = get_auth0_public_key()
            
            # Obter o cabeçalho do token para identificar a chave
            unverified_header = jwt.get_unverified_header(token)
            
            # Encontrar a chave correspondente no JWKS
            rsa_key = {}
            for key in jwks['keys']:
                if key['kid'] == unverified_header['kid']:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }
                    break
            
            if not rsa_key:
                return jsonify({'message': 'Chave não encontrada'}), 401
            
            # Verificar o token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUTH0_API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            
            # Se chegou até aqui, o token é válido
            # Adicionamos as informações do usuário ao objeto request
            request.current_user = payload
            
            return f(*args, **kwargs)
        
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.JWTClaimsError:
            return jsonify({'message': 'Claims inválidos. Verifique o audience e issuer'}), 401
        except Exception as e:
            return jsonify({'message': f'Erro na autenticação: {str(e)}'}), 401
            
    return decorated
