# Automação de Ingestão de Dados com n8n

Este projeto implementa uma automação completa para ingestão, transformação e análise de dados utilizando o n8n, MinIO, PostgreSQL e Python.

## Visão Geral
- **n8n**: Orquestra fluxos de automação para ingestão e transformação de dados.
- **MinIO**: Armazenamento de arquivos (S3 compatível).
- **PostgreSQL**: Banco de dados relacional para persistência dos dados.
- **Python**: Scripts para análise e transformação dos dados.

## Como usar

### 1. Configurando seu Arquivo .env
- **Atenção: Configure sempre suas próprias credenciais nos arquivos `.env` e nunca compartilhe dados sensíveis publicamente.**
- Crie o arquivo `.env` no Path `n8n-automation\n8n-compose` do projeto para armazenar variáveis sensíveis.
- Os nomes das variáveis devem ser iguais aos declarados no `docker-compose.yml`. Então adicione os seguintes nomes de variáveis no seu arquivo `.env`:
  ```env
  DOMAIN_NAME=seu_domínio_aqui # Para caso você queria configurar um DNS. Ex: marllonDev.com
  ```
  ```env
  SUBDOMAIN=seu_sub_domínio_aqui # Para caso você queria configurar um DNS, deverá pôr o seu sub domínio aqui, ex: n8n.
  ```
  > **Atenção:** Se os dois itens acima foram devidamente configurados, então o link final para acessar o n8n deveria ser assim: https://n8n.marllonDev.com.
  > 
  ```env
  GENERIC_TIMEZONE=America/Sao_Paulo # Para usar o Fuso de São Paulo - Brasil.
  ```
  ```env
  SSL_EMAIL=seu_email_aqui #Coloque seu e-mail que usará para fazer login na plataforma N8N. OBS: Use esse mesmo e-mail para fazer a criação da conta no N8N.
  ```
  ```env
  POSTGRES_USER=seu_nome_de_user_aqui # Coloque um nome de user para seu banco de dados.
  ```
  ```env
  POSTGRES_PASSWORD=sua_senha_aqui # Coloque uma senha de sua escolha para o seu banco de dados.
  ```
  ```env
  MINIO_ROOT_USER=seu_nome_de_user_aqui # Coloque um nome de user de sua escolha para o login no MinIo.
  ```
  ```env
  MINIO_ROOT_PASSWORD=sua_senha_aqui # Coloque uma senha de sua escolha para o login no MinIo.
  ```

  
- Para análise de dados, crie um `.env` dentro da pasta `\analise-dados` com os mesmos nomes usados no `main.ipynb`, mas substitua pelos seus próprios dados de acesso. 
  ```env
  MINIO_ENDPOINT=http://localhost:9000 # Esse é o endereço da qual o import s3 irá fazer a conexão
  ```
  ```env
  MINIO_ACCESS_KEY=seu_user_aqui # Add seu User aqui para o s3 fazer a conexão com o seu MinIo(pode pôr a mesma que cocolou no .env anterior)
  ```
   ```env
  MINIO_SECRET_KEY=sua_senha_aqui # Add sua senha aqui para o s3 fazer a conexão com o seu MinIo(pode pôr a mesma que cocolou no .env anterior)
  ```


### 2. Rodando o projeto
- A primeira coisa a se fazer após baixado o projeto, é navegar para a pasta `n8n-automation\n8n-compose`. Então rode o comando Docker para subir tudo:
  ```env
  docker compose up -d
  ```
- Você deverá ver todos os serviços ON no seu Terminal.


### 3. Gerando a N8N_ENCRYPTION_KEY
- A variável `N8N_ENCRYPTION_KEY` é obrigatória para criptografar credenciais e dados sensíveis no n8n.
- Para gerar uma chave segura, execute o comando abaixo no terminal:
  ```env
  docker exec -it n8n openssl rand -hex 32 
  ```
- Copie o resultado e cole na linha correspondente do seu arquivo `.env` no Path `n8n-automation\n8n-compose\.env`:
  ```env
  N8N_ENCRYPTION_KEY=coloque_o_valor_gerado_aqui
  ```
- Rode o comando docker abaixo para atualizar os seus contâiners com essa nova chave:
   ```bash
     docker compose down # Para parar para excluir os contâiners
   ```
   ```bash
     docker compose up -d # Para subir novamente os contâiners
   ```


### 4. Importando o Dataset para o PostgreSQL
- O arquivo `dump_funcionarios.sql` na pasta `backup/` contém um dump do banco de dados com 1 milhão de linhas.
- Para importar para dentro do container do banco:
  1. No terminal, navegue até a pasta `backup/`.
  2. Copie o dump para dentro do container usando a linha de comando abaixo:
     ```bash
     docker cp dump_funcionarios.sql postgres-db:/dump_funcionarios.sql
     ```
  3. Execute o comando dentro do container para restaurar o banco:
     ```bash
     docker exec -it postgres-db psql -U adm -d postgres -f /dump_funcionarios.sql
     ```
  4. Agora, 1 milhão de linhas estão dentro do banco pronto para você brincar.

     
### 5. Importando os Workflows do n8n
- Os arquivos `.json` na pasta `backup/` (ex: `Automation for Copy Data.json`, `Transformation To Parquet.json`) são workflows prontos do n8n.
- Para importar:
  1. Acesse a interface web do n8n (ex: http://localhost:5678/).
  2. Clique em **Create Workflow** no botão superior da direita.
  3. Com um Workflow em branco, clique nos três pontinhos, e depois em **Import from File** 
  4. Selecione o arquivo `Automation for Copy Data.json` da pasta `backup/`.
  5. Salve.
  6. Faça o mesmo para o outro arquivo.

### 6. Configurando credenciais no N8N
- Para adicionar a credencial do Postgres e do MinIo, basta navegar até a pasta `/backup/prints`. Os prints de como deve ficar estarão lá.
- Para adicionar cada credencial, você pode clicar duas vezes no Nó do **Postgres** e clicar em **Create new Credential**, depois é só seguir como nos prints. Faça o mesmo para o Nó do **Bucket S3**, que se encontra ao lado do Nó do Postgres.

### 7. Acessando o MinIO via Web
- O MinIO possui uma interface web para gerenciamento dos arquivos.
- Para acessar, abra o navegador e vá para: [http://localhost:9001](http://localhost:9001)
- Use as credenciais definidas no arquivo `.env`(`MINIO_ROOT_USER` e `MINIO_ROOT_PASSWORD`) do Path `n8n-automation\n8n-compose`.
- Após logado há dois buckets que devem ser criados:
  1. Para adicionar um novo bucket, clique no botão no canto superior esquerdo com o nome **Create Bucket**, e adicione o nome **raw-files-json**, então salve. Faça o mesmo para o outro bucket, mas o segundo deve ter o nome de **processed-parquet**.


### 8. Ajustando arquivo `s3_setup.sql`
- O arquivo nesse Path `\n8n-compose\local-files\s3_setup.sql`, deve ser confugurado adicionando as seguintes informações: 
 ```env
     s3_access_key_id = '' # Seu MINIO_ROOT_USER. O mesmo do arquivo .env.
 ```
 ```env
     s3_secret_access_key = '' # Seu Seu MINIO_ROOT_PASSWORD. O mesmo do arquivo .env.
 ```
- Os outros campos já viram preenchidos como devem ser.


### 9. Transformando os dados brutos em parquet
- Quando você colocar para rodar o workflow `Automation for Copy Data.json`, ele ira pegar de 10K em 10K do banco de dados, você pode deixar rodar por uns 5 minutos para pegar alguns dados consideraveis.
- Após isso, basta ir no outro workflow e colocar para rodar. Ele irá "chamar" o arquivo **transform.py**, onde está o código em Python que irá buscar os dados do MinIo, transforma-los em parquet e salvar no bucket de nome **processed-parquet**.
- Uma vez executado, você poderá entrar no bucket **processed-parquet**, e verá que os arquivos do bucket **raw-files-json** foram juntados em um só, e transformados em .parquet. Um formato mais leve. Pode reparar isso vendo no Header dos dois buckets, o somatórios de todos os arquivos que estão em cada um.


### 10. Fazendo a Análise de Dados
- Por último, foi criado um arquivo no Path `n8n-automation\analise-dados\main.ipynb`, onde você vai usar o VS Code ou outra IDE de seu interesse para rodar um simples código de análise, ou seja, o início de tudo que é a configuração com o MinIo, e depois disso um SELECT para vermos o que há naquele arquivo.
- Para rodar esse arquivo, é interessante que você tenha a extensão **Jupyter** que pode ser baixada no VS Code. Com ele instalado, você pode rodar o arquivo Célula por Célula ou clicar no "Run all" para rodar tudo de uma vez.
- Para rodar isso em um enviroment separado, vá a pasta `n8n-automation\analise-dados\` usando o comando CD do terminal e crie uma variável de ambiente. Siga os comandos abaixo para isso:
    1. ```env
       python -m venv .venv
         ```
    2. Agora, vamos ativar o seu enviroment com o seguinte comando:
       1. No CMD do Win, use esse comando:
           ```env
           .\.venv\Scripts\activate
             ```
       2. No Linux e no Mac, use o seguinte comando
             ```env
           source .venv/bin/activate
             ```
    4. Com o .venv ativado, vamos baixar alguns módulos que seram instaladas dentro do .venv somente. Rode o comando abaixo:
       ```env
       pip install pandas s3fs python-dotenv pyarrow fastparquet
         ```
    5. Agora, precisamos instalar o "motor" do Jupyter, então rode o comando abaixo:
        ```env
       pip install ipykernel
         ```
    6. Agora, vamos "apresentar" formalmente o nosso ambiente para o sistema Jupyter do seu computador, dando a ele um nome amigável que aparecerá na lista de opções. Rode o comando abaixo:
        ```env
       python -m ipykernel install --user --name="analise-dados-venv" --display-name="Python (Análise de Dados)"
         ```
    7. Vamos selecionar o kernel correto então:
       1. Reinicie o VS Code para garantir que ele detecte o novo kernel que acabamos de registrar.
       2. Abra seu arquivo .ipynb.
       3. No canto superior direito, clique no nome do kernel atual ou no botão "Select Kernel".
       4. Na lista que aparecer, procure e selecione o nome amigável que definimos: Python (Análise de Dados).
        
- NOTA: Se ao rodar a última Célula e dar o seguinte **ERRO: Não foi possível ler o arquivo. Verifique o caminho, as credenciais e o endpoint.Detalhe do erro: No type extension with name arrow.py_extension_type found**, então rode o comando:
  ```env
       pip install --upgrade pandas pyarrow s3fs python-dotenv
  ```
- Dê um Restart no Kernel e depois coloque para rodar novamente.
- Após rodar o SELECT verá que tem duas novas colunas, a coluna de "ID" e a "Criado em". Foram criadas somente essas duas para manter a coisa simples, mas em um projeto grande de Dados, podem ser adicionadas várias colunas com diferentes critérios. Isso é o enrriquecimento do dado.


  ## Agora os próximos passos são com você, use sua imaginação para fazer mais análise desses dados, afinal, você tem um banco com 1 milhão de registros. Tenho certeza que da pra fazer muita coisa com isso. Me despeço, dizendo que foi um prazer produzir esse projeto para o pessoal da área e curiosos. Até mais vê.




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


![Logo](https://media.licdn.com/dms/image/v2/D4D03AQEFlFTNmApBhQ/profile-displayphoto-shrink_800_800/B4DZbt9iTrHsAc-/0/1747749054334?e=1756944000&v=beta&t=NW8glGWRr3nju_eTn_S49tng936yy-t1pxHxTU0JZ38)

---
