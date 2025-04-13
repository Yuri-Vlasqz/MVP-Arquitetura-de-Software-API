# MVP-Arquitetura-de-Software-API

Este repositório contém a implementação do back-end do **MVP** (_Minimum Viable Product_) da _Sprint_ de **Arquitetura de Software** do Curso de Engenharia de Software da PUC-Rio.
A parte do front-end pode ser acessada em [MVP-Arquitetura-de-Software-Interface](https://github.com/Yuri-Vlasqz/MVP-Arquitetura-de-Software-Interface)

No contexto da crescente variedade de serviços de streaming e da variação de conteúdo de acordo com a localização geográfica, foi criado esse projeto:
> A aplicação web, **"Tudo a ver 2.0"**, permite a busca de séries e filmes disponíveis em todas plataformas de _streaming_ de qualquer país. Além disso, ao fazer o login, cada usuário pode criar e customizar, de forma protegida, suas próprias listas de programas, descobrindo em um clique, onde assistir em qualquer lugar que estiver.


## Arquitetura da aplicação:

<p align="center">
  <img src="assets/Fluxograma%20de%20arquitetura%20de%20MVP.png">
</p>
<h6 align="center">Fluxograma - Cenário 1.1</h6>


#### O contêiner Python representa o conteúdo deste repositório:
- A comunicação da API com o Interface SPA é feita seguindo o padrão _REST_.
- A consulta de dados sobre filmes e séries é feita utilizando o serviço externo, _The Movie Data Base_.
- A consulta de autenticação, dos tokens de acesso de usuários, é feita utilizando o serviço externo, _Auth0_.
- Os registros de informações de usuários, listas e programas são salvos no banco de dados local _SQlite_.

#### O contêiner Node.js representa o conteúdo do repositório [MVP-Arquitetura-de-Software-Interface](https://github.com/Yuri-Vlasqz/MVP-Arquitetura-de-Software-Interface)
<br>

## Rotas da API REST:

#### Rotas com chamadas a API externa TMDB
| **URL da rota** | **Método** | **Descrição da ação**                                                                                                | **Status de respostas documentados** |
|-----------------|------------|----------------------------------------------------------------------------------------------------------------------|--------------------------------|
| /search         | GET        | Busca possíveis resultados de programas, a partir do nome.                                                           | 200, 400                       |
| /details        | GET        | Busca de informações e provedores de um programa, a partir do id TMDB e tipo de mídia.                               | 200, 400                       |


#### Rotas protegidas da API
| **URL da rota** | **Método** | **Descrição da ação**                                                                                                   | **Status de respostas documentados** |
|-----------------|------------|-------------------------------------------------------------------------------------------------------------------------|--------------------------------|
| /lista          | POST       | Adiciona uma nova lista atrelada a um usuário, a partir do id do usuário e nome da lista.                               | 201, 401, 404, 409, 500        |
| /lista          | PUT        | Atualiza informações de uma lista, a partir do id.                                                                      | 200, 401, 404, 409, 500        |
| /lista          | DELETE     | Deleta uma lista, a partir do id.                                                                                       | 200, 401, 404, 500             |
| /programa-lista | POST       | Adiciona uma associação entre um programa e uma lista, a partir de seus id's. OBS: Cria um programa se ele não existir. | 201, 401, 404, 409, 500        |
| /programa-lista | DELETE     | Remove uma associação entre um programa e uma lista, a partir de seus id's.                                             | 200, 401, 404, 500             |
| /usuario        | GET        | Busca por um usuário, a partir do email.                                                                                | 200, 401, 404, 500             |
| /usuario        | POST       | Cria um usuário a partir do email, com as listas padrão (Favoritos, Assistidos, Próximos a ver).                        | 201, 401, 409, 500             |
<br>

## Tecnologias principais

Para executar o projeto, você precisará ter instalado:
- [Python 3.12](https://www.python.org/);
- [Flask[async]](https://flask.palletsprojects.com/) para construção da API com requisições assíncronas;
- [flask-openapi3-swagger](https://luolingchun.github.io/flask-openapi3/v4.x/) para a documentação em `Swagger` da API;
- [aiohttp](https://docs.aiohttp.org/en/stable/) para chamadas concorrentes ao TMDB;
- [SQLAlchemy](https://www.sqlalchemy.org/) para modelagem do banco de dados SQlite;

<br>

## Configuração das API`s externas 

#### Configuração do TMDB para obter informações de programas:
1. Crie uma conta no [TMDB](https://www.themoviedb.org/)
2. siga as instruções para [obtenção da chave de api](https://developer.themoviedb.org/docs/getting-started) e obtenha o valor:
    - `Token de Leitura da API`


#### Configuração do Auth0 para proteger rotas:
1. Crie uma conta no [Auth0](https://auth0.com/).
2. Configure uma aplicação do tipo API ou _Auth0 Management API_ no painel Auth0 e obtenha esses valores:
   - `Domain`
   - `API Identifier`


## Configuração das variaveis de ambiente
No diretório raiz do repositório, crie o arquivo `.env` e preencha com os valores obtidos nas API`s externas, conforme abaixo:
```
AUTH0_DOMAIN="Domain"
AUTH0_API_AUDIENCE="API Identifier"
TMDB_API_KEY="Token de Leitura da API"
```
<br>

## Instalação e Execução

**Clone este repositório pela URL, e siga as intruções para uma das formas de executar a API.**


#### Execução pelo ambiente virtual do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html):

1. No diretório raiz do repositório, pelo terminal, execute o comando abaixo para criar um ambiente virtual. 
    ```
    python -m venv .venv
    ```
    
2. Ative o ambiente virtual.
    ```
    .venv\Scripts\activate
    ```

3. Instale todas as dependências/bibliotecas python listadas no `requirements.txt` no ambiente virtual. 
    ```
    pip install -r requirements.txt
    ```

4. Execute a API:
    ```
    flask run --host 0.0.0.0 --port 5000
    ```

    Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
    automaticamente após uma mudança no código fonte. 

    ```
    flask run --host 0.0.0.0 --port 5000 --reload
    ```
<br>

#### Execução pelo arquivo Dockerfile, através do [Docker](https://www.docker.com/):

1. No diretório raiz do repositório, pelo terminal, crie a imagem do código:
   ```
   docker build -t mvp_api .
   ```

2. Execute a imagem criada no Docker:
   ```
   docker run -p 5000:5000 mvp_api
   ```
<br>

#### Verifique a API em execução:

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar a documentação em `Swagger`. Para testar rotas protegidas, adicione o token Auht0 no campo `Authorize 🔒`.
> **OBS:** Para obter um token de teste, siga as intruções: [accessar tokens de teste](https://auth0.com/docs/secure/tokens/access-tokens/management-api-access-tokens/get-management-api-access-tokens-for-testing)
