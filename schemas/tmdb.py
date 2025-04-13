from pydantic import BaseModel

from datetime import date
from typing import Optional, List, Dict


class TmdbBuscaSchema(BaseModel):
	""" Estrutura da consulta de programa no TMDB.
	"""
	nome: str = 'De Volta para o Futuro'


class TmdbBuscaDetalhesSchema(BaseModel):
	""" Estrutura de consulta de detalhes de um programa no TMDB.
	"""
	tmdb_id: int = 105
	tipo: str = 'movie'


class TmdbResultadoSchema(BaseModel):
	""" Estrutura de programa no TMDB.
	"""
	tmdb_id: int
	tipo: str
	titulo: str
	titulo_original: str
	lancamento: date
	resumo: str
	url_poster: Optional[str]


class TmdbListagemResultadoSchema(BaseModel):
	""" Estrutura de listagem de programas no TMDB.
	"""
	filmes: List[TmdbResultadoSchema]
	numero_filmes: int
	series: List[TmdbResultadoSchema]
	numero_series: int


def apresenta_resultados_busca(resultados_filmes, resultados_series) -> TmdbListagemResultadoSchema:
	""" Apresente os resultados da busca de acordo com TmdbListagemResultadoSchema.
	"""
	num_filmes = len(resultados_filmes)
	num_series = len(resultados_series)

	filmes = []
	series = []
	for filme in resultados_filmes:
		filmes.append({
			'tmdb_id': filme.get('id'),
			'tipo': 'movie',
			'titulo': filme.get('title'),
			'titulo_original': filme.get('original_title'),
			'lancamento': filme.get('release_date'),
			'resumo': filme.get('overview'),
			'url_poster': filme.get('poster_path'),
		})

	for serie in resultados_series:
		series.append({
			'tmdb_id': serie.get('id'),
			'tipo': 'tv',
			'titulo': serie.get('name'),
			'titulo_original': serie.get('original_name'),
			'lancamento': serie.get('first_air_date'),
			'resumo': serie.get('overview'),
			'url_poster': serie.get('poster_path'),
		})

	return {
		'filmes': filmes,
		'numero_filmes': num_filmes,
		'series': series,
		'numero_series': num_series
		}


class TmdbProvedorSchema(BaseModel):
	""" Estrutura de uma provedor de um programa no TMDB.
	"""
	nome: str
	url_logo: Optional[str]


class TmdbDetalhesSchema(BaseModel):
	""" Estrutura de detalhes de um programa no TMDB.
	
		OBS: Provedores locais são obtidos pela sigla do pais. 
		Ex: provedores_mundiais['BR'].
	"""
	tmdb_id: int
	tipo: str
	titulo: str
	titulo_original: str
	lancamento: date
	resumo: str
	generos: List[Optional[str]]
	url_poster: Optional[str]
	duracao: str
	tagline: Optional[str]	
	provedores_mundiais: Dict[str, List[Optional[TmdbProvedorSchema]]]


def apresenta_detalhes_programa(detalhes_tmdb, provedores_tmdb, tipo, local='BR') -> TmdbDetalhesSchema:
	"""	Combina as respostas aos endpoints '/details' e '/watch/providers', do TMDB, em um dicionário.
	"""
	if tipo == 'movie':
		lancamento = detalhes_tmdb.get('release_date')
		titulo = detalhes_tmdb.get('title')
		titulo_original = detalhes_tmdb.get('original_title')
		if detalhes_tmdb.get('runtime'):
			if detalhes_tmdb.get('runtime') > 60:
				duracao = '{:01d}h {:02d}m'.format(*divmod(detalhes_tmdb.get('runtime'), 60))
			else:
				duracao = '{:01d}m'.format(detalhes_tmdb.get('runtime'))
		else:
			duracao = 'N/A'
		
	if tipo == 'tv':
		lancamento = detalhes_tmdb.get('first_air_date')
		titulo = detalhes_tmdb.get('name')
		titulo_original = detalhes_tmdb.get('original_name')
		duracao = detalhes_tmdb.get('number_of_seasons')

	lista_generos = [genero.get('name') for genero in detalhes_tmdb.get('genres', [])]

	poster_path = detalhes_tmdb.get('poster_path')
	poster_url = f"https://image.tmdb.org/t/p/w342{poster_path}" if poster_path else None

	provedores_mundiais = {}
	base_image_url = "https://image.tmdb.org/t/p/w185"
	for pais, info in provedores_tmdb.get("results", {}).items():
		# flatrate = streaming por assinatura
		provedores_locais = info.get("flatrate", [])
		provedores_mundiais[pais] = [
			{
				"nome": provedor.get("provider_name"),
				"url_logo": base_image_url + provedor.get("logo_path") if provedor.get("logo_path") else None
			}
			for provedor in provedores_locais
		]

	return {
		'tmdb_id': detalhes_tmdb.get('id'),
		'tipo': tipo,
		'titulo': titulo,
		'titulo_original': titulo_original,
		'lancamento': lancamento,
		'resumo': detalhes_tmdb.get('overview'),
		'generos': lista_generos,
		'duracao': duracao,
		'url_poster': poster_url,
		'tagline': detalhes_tmdb.get('tagline'),
		'provedores_mundiais': provedores_mundiais
	}
