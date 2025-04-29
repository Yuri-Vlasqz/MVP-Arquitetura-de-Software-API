# Define a imagem base
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte para o diretório de trabalho
COPY . .

EXPOSE 5000

# --- Define o comando de execução da API ---

# Servidor de desenvolvimento Flask
# CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]

# Servidor WSGI de produção Gunicorn
# CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]

# Servidor WSGI de produção Gunicorn com o arquivo de configuração
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]