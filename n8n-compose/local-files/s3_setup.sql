-- Nome do arquivo: s3_setup.sql
INSTALL s3;
LOAD s3;
SET s3_endpoint = 'http://minio:9000';
SET s3_url_style = 'path';
SET s3_access_key_id = 'adm'; -- Seu MINIO_ROOT_USER
SET s3_secret_access_key = 'meuMinIo'; -- Seu MINIO_ROOT_PASSWORD