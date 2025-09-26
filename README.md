# Pré-requisitos
## Baixar os dados
Os dados não estão incluídos no repositório devido ao tamanho. Baixe o arquivo usando:
```sh
# Baixar do SNAP Stanford (fonte original)
curl -o data/amazon-meta.txt.gz https://snap.stanford.edu/data/bigdata/amazon/amazon-meta.txt.gz

# Descompactar o arquivo (opcional, o script faz isso automaticamente)
gunzip data/amazon-meta.txt.gz
```

# 1) Construir e subir os serviços
```sh
docker compose up -d --build
```
# 2) (Opcional) conferir saúde do PostgreSQL
```sh
docker compose ps
```
# 3) Criar esquema e carregar dados
**Nota:** Certifique-se de ter baixado os dados primeiro (veja seção "Pré-requisitos" acima)
```sh
docker compose run --rm app python src/tp1_3.2.py \
  --db-host db --db-port 5432 --db-name ecommerce --db-user postgres --db-pass postgres \
  --input /data/snap_amazon.txt
```
# 4) Executar o Dashboard (todas as consultas)
```sh
docker compose run --rm app python src/tp1_3.3.py \
  --db-host db --db-port 5432 --db-name ecommerce --db-user postgres --db-pass postgres \
  --output /app/out
```
# 5) Reproduzir do zero
```sh
docker compose down -v
```
