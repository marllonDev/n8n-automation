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

### 2. Acessando o MinIO via Web
- O MinIO possui uma interface web para gerenciamento dos arquivos.
- Para acessar, abra o navegador e vá para: [http://localhost:9001](http://localhost:9001)
- Use as credenciais definidas no arquivo `.env` (`MINIO_ROOT_USER` e `MINIO_ROOT_PASSWORD`).

### 3. Gerando a N8N_ENCRYPTION_KEY
- A variável `N8N_ENCRYPTION_KEY` é obrigatória para criptografar credenciais e dados sensíveis no n8n.
- Para gerar uma chave segura, execute o comando abaixo no terminal:
  ```bash
  openssl rand -hex 32
  ```
- Copie o resultado e cole na linha correspondente do seu arquivo `.env`:
  ```env
  N8N_ENCRYPTION_KEY=coloque_o_valor_gerado_aqui
  ```

### 4. Importando o Dataset para o PostgreSQL
- O arquivo `dump_funcionarios.sql` na pasta `backup/` contém um dump do banco de dados com 1 milhão de linhas.
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

### 5. Segurança e Boas Práticas
- **Nunca compartilhe suas credenciais!**
- Crie arquivos `.env` no seu projeto para armazenar variáveis sensíveis.
- Os nomes das variáveis devem ser iguais aos declarados no `docker-compose.yml` para subir os serviços.
- Para análise de dados, crie um `.env` dentro da pasta `analise-dados` com os mesmos nomes usados no `main.ipynb`, mas substitua pelos seus próprios dados de acesso.

> **Atenção:** Configure sempre suas próprias credenciais nos arquivos `.env` e nunca compartilhe dados sensíveis publicamente.

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
## Sobre mim
𝐒𝐞𝐧𝐢𝐨𝐫 𝐃𝐚𝐭𝐚 𝐄𝐧𝐠𝐢𝐧𝐞𝐞𝐫

Com 𝟰+ 𝘆𝗲𝗮𝗿𝘀 de experiência no mundo da tecnologia, eu me desenvolvo na interseção entre engenharia de dados e inovação. Atualmente, estou criando ecossistemas de dados escaláveis como 𝗦𝗲𝗻𝗶𝗼𝗿 𝗗𝗮𝘁𝗮 𝗘𝗻𝗴𝗶𝗻𝗲𝗲𝗿. Aperfeiçoei minhas habilidades em setores que moldam as economias - desde 𝗺𝗮𝗶𝗼𝗿𝗲𝘀 𝗯𝗮𝗻𝗰𝗼𝘀 𝗱𝗼 𝗕𝗿𝗮𝘀𝗶𝗹 e 𝘀𝗲𝗴𝘂𝗿𝗮𝗱𝗼𝗿𝗮𝘀 𝗹𝗶𝗱𝗲𝗿𝗲𝘀 𝗺𝘂𝗻𝗱𝗶𝗮𝗶𝘀, até o 𝗺𝗮𝗶𝗼𝗿 𝗽𝗿𝗼𝗱𝘂𝘁𝗼𝗿 𝗱𝗲 𝗰𝗲𝗿𝘃𝗲𝗷𝗮 do mundo, e agora estou causando impacto no 𝘀𝗲𝘁𝗼𝗿 𝗱𝗼 𝗰𝗿𝗲𝗱𝗶𝘁𝗼. 

💡 𝗣𝗼𝗿𝗾𝘂𝗲 𝗲𝘂 𝗺𝗲 𝗱𝗲𝘀𝘁𝗮𝗰𝗼? \
Eu 𝗮𝗿𝗾𝘂𝗶𝘁𝗲𝘁𝗼 𝗽𝗶𝗽𝗲𝗹𝗶𝗻𝗲𝘀 de dados robustos para 𝗙𝗼𝗿𝘁𝘂𝗻𝗲 𝟱𝟬𝟬 𝗽𝗹𝗮𝘆𝗲𝗿𝘀, otimizei os sistemas legados para nuvem (𝗔𝗪𝗦/𝗔𝘇𝘂𝗿𝗲) que forneceram insights acionáveis por meio de estruturas ETL/ELT escaláveis. Da análise financeira em tempo real à otimização da cadeia de suprimentos de cervejarias, eu transformo dados brutos em ativos estratégicos. 

✨ 𝗔𝗹𝗲𝗺 𝗱𝗼 𝗰𝗼𝗱𝗶𝗴𝗼: \
Um aprendiz permanente obcecado com a democratização de dados e a solução ágil de problemas. Vamos nos conectar se você estiver 𝗮𝗽𝗮𝗶𝘅𝗼𝗻𝗮𝗱𝗼 sobre a nuvem, eficiência do 𝗗𝗲𝘃𝗢𝗽𝘀 ou o papel dos dados na transformação dos setores!

Me siga: [Linkedin](https://www.linkedin.com/in/marllonzuc/) \
Meu Blog: [Blog](https://datatrends.me/)


![Logo](https://media.licdn.com/dms/image/v2/D4D03AQEFlFTNmApBhQ/profile-displayphoto-shrink_800_800/B4DZbt9iTrHsAc-/0/1747749054334?e=1753315200&v=beta&t=VfBvrDxLmoAYccE0DW63MbSLz_ao9Xp_HQAfcyP7-og)

---