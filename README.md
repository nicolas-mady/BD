# Pré-requisitos
## Baixar os dados
Os dados não estão incluídos no repositório devido ao tamanho. Baixe o arquivo usando:
```sh
# Baixar do SNAP Stanford (fonte original)
curl -o data/amazon-meta.txt.gz https://snap.stanford.edu/data/bigdata/amazon/amazon-meta.txt.gz

# Ou usando wget
wget -O data/amazon-meta.txt.gz https://snap.stanford.edu/data/bigdata/amazon/amazon-meta.txt.gz

# Descompactar o arquivo (opcional, o script faz isso automaticamente)
gunzip data/amazon-meta.txt.gz
```

**Nota:** O arquivo tem aproximadamente 210MB comprimido e contém metadados e reviews de ~548,552 produtos da Amazon coletados em 2006.

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

## Problemas comuns
### Arquivo de dados não encontrado
Se você não conseguir baixar o arquivo original, pode usar dados alternativos:
- Procure por datasets similares no [SNAP Stanford](https://snap.stanford.edu/data/)
- Use qualquer arquivo de dados da Amazon no formato correto
- O script tentará baixar automaticamente se o arquivo não for encontrado

### Arquivo muito grande para Git
Este projeto usa `.gitignore` para excluir arquivos grandes. Em outras máquinas:
1. Clone o repositório
2. Baixe os dados usando os comandos na seção "Pré-requisitos"
3. Execute normalmente
