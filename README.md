# Automação de Ingestão de Dados com n8n

Este projeto implementa uma automação completa para ingestão, transformação e análise de dados utilizando o n8n, MinIO, PostgreSQL e Python.

## Visão Geral
- **n8n**: Orquestra fluxos de automação para ingestão e transformação de dados.
- **MinIO**: Armazenamento de arquivos (S3 compatível).
- **PostgreSQL**: Banco de dados relacional para persistência dos dados.
- **Python**: Scripts para análise e transformação dos dados.

## Como usar

### 1. Importando os Workflows do n8n
- Os arquivos `.json` na pasta `backup/` (ex: `Automation for Copy Data.json`, `Transformation To Parquet.json`) são workflows prontos do n8n.
- Para importar:
  1. Acesse a interface web do n8n (ex: http://localhost:5678/).
  2. Clique em **Importar** (ícone de upload) no menu superior.
  3. Selecione o arquivo `.json` desejado da pasta `backup/`.
  4. Salve e execute o workflow.

### 2. Importando o Dataset para o PostgreSQL
- O arquivo `n8n-compose_postgres_db_data.tar.gz` na pasta `backup/` contém um dump do banco de dados com 1 milhão de linhas.
- Para importar para dentro do container do banco:
  1. No terminal, navegue até a pasta `backup/`:
     ```bash
     cd /caminho/para/backup
     ```
  2. Copie o dump para dentro do container:
     ```bash
     docker cp dump_funcionarios.sql postgres-db:/dump_funcionarios.sql
     ```
  3. Execute o comando dentro do container para restaurar o banco:
     ```bash
     docker exec -it postgres-db psql -U adm -d postgres -f /dump_funcionarios.sql
     ```

### 3. Segurança e Boas Práticas
- **Nunca compartilhe suas credenciais!**
- Crie arquivos `.env` no seu projeto para armazenar variáveis sensíveis.
- Os nomes das variáveis devem ser iguais aos declarados no `docker-compose.yml` para subir os serviços.
- Para análise de dados, crie um `.env` dentro da pasta `analise-dados` com os mesmos nomes usados no `main.ipynb`, mas substitua pelos seus próprios dados de acesso.

## Estrutura do Projeto
```
analise-dados/
  main.ipynb
  .env
backup/
  Automation for Copy Data.json
  Transformation To Parquet.json
  n8n-compose_postgres_db_data.tar.gz
n8n-compose/
  docker-compose.yml
  n8n.Dockerfile
  .env
  local-files/
    s3_setup.sql
    transform.py
```

## .gitignore Sugerido
```
.venv/
.env/
*.pyc
__pycache__/
*.tar.gz
analise-dados/.env
n8n-compose/.env
```

---

> **Atenção:** Configure sempre suas próprias credenciais nos arquivos `.env` e nunca compartilhe dados sensíveis publicamente.
