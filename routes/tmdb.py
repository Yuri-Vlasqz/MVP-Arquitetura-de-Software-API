import asyncio, aiohttp
from flask_openapi3 import APIBlueprint, Tag
from dotenv import load_dotenv
from schemas import *
import os

tmdb_tag = Tag(name="TMDB - API externa", description="Chamadas ao TMDB para obtenção de informações de programas")
tmdb_bp = APIBlueprint('tmdb', __name__, url_prefix='/api', abp_tags=[tmdb_tag])

load_dotenv()
# Configurações TMDB
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
LANGUAGE = "pt-BR"
BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_API_KEY}"
}


@tmdb_bp.get('/search',
    responses={"200": TmdbListagemResultadoSchema, "400": ErrorSchema})
async def search(query: TmdbBuscaSchema):
    """ Busca possíveis resultados de programas, a partir do nome.
    """	
    query = query.nome
    params = {
        "query": query,
        "include_adult": "false",
        "language": LANGUAGE
    }
    endpoints = {
        "movies": f"{BASE_URL}/search/movie",
        "tv_shows": f"{BASE_URL}/search/tv"
    }

    async with aiohttp.ClientSession(headers=HEADERS) as aio_session:
        tasks = {
            name: aio_session.get(url=url, params=params)
            for name, url in endpoints.items()
        }
        try:
            responses = await asyncio.gather(*tasks.values())
            results = {}
            for name, response in zip(tasks.keys(), responses):
                data = await response.json()
                results[name] = data.get('results', [])

            return apresenta_resultados_busca(results['movies'], results['tv_shows']), 200

        except Exception as e:
            return {"mensagem": str(e)}, 400


@tmdb_bp.get('/details',
    responses={"200": TmdbDetalhesSchema, "400": ErrorSchema})
async def details(query: TmdbBuscaDetalhesSchema):
    """ Busca de informações e provedores de um programa, a partir do id na TMDB e tipo de mídia.
    """
    tmdb_id = query.tmdb_id
    tipo = query.tipo
    params = {
        "language": LANGUAGE
    }
    endpoints = {
        "details": f"{BASE_URL}/{tipo}/{tmdb_id}",
        "watch_providers": f"{BASE_URL}/{tipo}/{tmdb_id}/watch/providers"
    }

    async with aiohttp.ClientSession(headers=HEADERS) as aio_session:
        tasks = {
            key: aio_session.get(url=url, params=params)
            for key, url in endpoints.items()
        }
        try:
            responses = await asyncio.gather(*tasks.values())
            results = {}
            for key, response in zip(tasks.keys(), responses):
                results[key] = await response.json()

            return apresenta_detalhes_programa(results['details'], results['watch_providers'], tipo), 200
        
        except Exception as e:
            return {"mensagem": str(e)}, 400
