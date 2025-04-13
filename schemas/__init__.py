from schemas.error import ErrorSchema
from schemas.usuario import UsuarioBuscaEmailSchema, UsuarioPostSchema, \
                            UsuarioResponseSchema, UsuarioViewSchema, \
                            mensagem_resposta_usuario, apresenta_usuario
from schemas.lista import ListaBuscaIdSchema, ListaPostSchema, ListaPutSchema, ListaResponseSchema, \
                          ListaViewSchema, mensagem_resposta_lista, apresenta_lista
from schemas.programa import ProgramaViewSchema, apresenta_programa
from schemas.lista_programa import ListaProgramaBuscaSchema, ListaProgramaPostSchema, \
                                   ListaProgramaResponseSchema, mesagem_resposta_lista_programa
from schemas.tmdb import TmdbBuscaSchema, TmdbBuscaDetalhesSchema, TmdbListagemResultadoSchema, \
                             TmdbProvedorSchema, TmdbDetalhesSchema, apresenta_resultados_busca, \
                             apresenta_detalhes_programa