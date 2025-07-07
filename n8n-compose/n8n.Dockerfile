
FROM docker.n8n.io/n8nio/n8n:latest

# Instala dependências do sistema e Python
USER root
RUN apk add --no-cache python3 py3-pip build-base

# Instala bibliotecas Python necessárias para automação de dados
RUN pip install pandas pyarrow s3fs --break-system-packages

USER node