import os
import re
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

MENU = '''
0. Sair
1. Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação.
2. Dado um produto, listar os produtos similares com maiores vendas (melhor salesrank) do que ele.
3. Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do período coberto no arquivo.
4. Listar os 10 produtos líderes de venda em cada grupo de produtos.
5. Listar os 10 produtos com a maior média de avaliações úteis positivas por produto.
6. Listar as 5 categorias com a maior média de avaliações úteis positivas por produto.
7. Listar os 10 clientes que mais fizeram comentários por grupo de produto.
'''


def main():
    usr = os.getenv('PG_USER', 'postgres')
    pwd = os.getenv('PG_PASSWORD', 'postgres')
    host = os.getenv('PG_HOST', 'localhost')
    port = os.getenv('PG_PORT', '5432')
    db = os.getenv('PG_DB', 'ecommerce')
    db_url = f"postgresql://{usr}:{pwd}@{host}:{port}/{db}"
    engine = create_engine(db_url)

    *sqls, _ = sorted(os.listdir('../sql'))
    stmts = [open(f'../sql/{f}').read() for f in sqls]

    print(MENU)
    while True:
        try:
            opt = int(input('\nEscolha uma opção:\n'))
        except ValueError:
            print("Por favor, insira um número válido.")
            continue
        if opt == 0:
            break
        if 1 <= opt <= 7:
            stmt = stmts[opt - 1]
            if opt <= 3:
                pasin = '0807220280'
                stmt = re.sub(r"pasin = '\w*'", f"pasin = '{pasin}'", stmt)
            print(pd.read_sql(stmt, engine))
        else:
            print('Opção inválida! Tente novamente.')


if __name__ == '__main__':
    load_dotenv()
    main()
