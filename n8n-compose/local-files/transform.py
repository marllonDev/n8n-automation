# Nome do arquivo: transform.py (Versão Robusta)
import os
import pandas as pd
import s3fs
from datetime import datetime
import uuid

# --- Configuração do MinIO ---
# Pegamos as credenciais das variáveis de ambiente que o Docker Compose passa.
MINIO_ENDPOINT = 'http://minio:9000'
MINIO_ACCESS_KEY = os.getenv('MINIO_ROOT_USER')
MINIO_SECRET_KEY = os.getenv('MINIO_ROOT_PASSWORD')

# IMPORTANTE: Verifique se este nome é EXATAMENTE igual ao seu bucket no MinIO.
SOURCE_BUCKET = 'raw-files-json'
DESTINATION_BUCKET = 'processed-parquet'

print(">>> Iniciando script de transformação com Python (Versão Robusta)...")

try:
    # 1. Cria um objeto de sistema de arquivos para se comunicar com o MinIO.
    s3 = s3fs.S3FileSystem(
        key=MINIO_ACCESS_KEY,
        secret=MINIO_SECRET_KEY,
        client_kwargs={'endpoint_url': MINIO_ENDPOINT}
    )

    # 2. Pede ao MinIO a lista de TODOS os arquivos .json dentro do bucket de origem.
    # A função glob expande o caractere curinga '*'
    source_files_path = f"{SOURCE_BUCKET}/*.json"
    print(f">>> Procurando por arquivos em: {source_files_path}")
    
    # s3.glob() retorna uma lista de todos os arquivos que correspondem ao padrão.
    all_json_files = s3.glob(source_files_path)
    
    # Adicionamos o protocolo 's3://' para o pandas ler corretamente
    s3_paths = [f"s3://{f}" for f in all_json_files]

    if not s3_paths:
        raise FileNotFoundError(f"Nenhum arquivo .json encontrado em {SOURCE_BUCKET}")

    print(f">>> {len(s3_paths)} arquivos encontrados. Lendo e concatenando...")

    # 3. Lê cada arquivo JSON da lista e os junta em uma única tabela (DataFrame).
    # O pd.concat junta múltiplas tabelas em uma só.
    df = pd.concat([pd.read_json(p, storage_options=s3.storage_options) for p in s3_paths], ignore_index=True)
    
    print(f">>> {len(df)} linhas lidas no total.")

    df.columns = df.columns.str.upper()
    print(">>> Nomes das colunas convertidos para caixa alta.")

    # --- AQUI ACONTECE A TRANSFORMAÇÃO ---
    print(">>> Aplicando transformações...")
    df['ID'] = [str(uuid.uuid4()) for _ in range(len(df))]
    df['CRIADO EM'] = datetime.utcnow()
    print(">>> Colunas 'ID' e 'CRIADO EM' adicionadas.")
    
    # --- FIM DA TRANSFORMAÇÃO ---

    # 4. Salva o DataFrame transformado como um único arquivo Parquet.
    output_file = f"s3://{DESTINATION_BUCKET}/dados_tratados.parquet"
    print(f">>> Salvando arquivo Parquet em: {output_file}")
    df.to_parquet(
        output_file,
        engine='pyarrow',
        compression='zstd',
        storage_options=s3.storage_options
    )
    print(">>> Script finalizado com sucesso!")

except Exception as e:
    print(f"ERRO: Ocorreu um erro durante a execução do script: {e}")
    raise e