import argparse
import os
import re
import sys
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='PostgreSQL database dashboard for Amazon data analysis')
    parser.add_argument('--db-host', default=os.getenv('PG_HOST', 'localhost'),
                        help='Database host (default: localhost)')
    parser.add_argument('--db-port', default=os.getenv('PG_PORT', '5432'),
                        help='Database port (default: 5432)')
    parser.add_argument('--db-name', default=os.getenv('PG_DB', 'ecommerce'),
                        help='Database name (default: ecommerce)')
    parser.add_argument('--db-user', default=os.getenv('PG_USER', 'postgres'),
                        help='Database user (default: postgres)')
    parser.add_argument('--db-pass', default=os.getenv('PG_PASSWORD', 'postgres'),
                        help='Database password (default: postgres)')
    parser.add_argument('--product-asin', default='0807220280',
                        help='Product ASIN for queries that require a specific product (default: 0807220280)')
    parser.add_argument('--output', default='/app/out',
                        help='Output directory for CSV files and reports (default: /app/out)')
    return parser.parse_args()


args = parse_arguments()

# Criar diretório de saída se não existir
os.makedirs(args.output, exist_ok=True)

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
    db_url = f"postgresql://{args.db_user}:{args.db_pass}@{args.db_host}:{args.db_port}/{args.db_name}"
    engine = create_engine(db_url)

    *sqls, _ = sorted(os.listdir('/app/sql'))
    stmts = [open(f'/app/sql/{f}').read() for f in sqls]
    csv_filenames = [re.sub(r'\.sql$', '.csv', f) for f in sqls]
    query_titles = [
        "Top 5 comentários mais úteis (maior e menor avaliação)",
        "Produtos similares com maiores vendas",
        "Evolução diária das médias de avaliação",
        "10 produtos líderes de venda por grupo",
        "10 produtos com maior média de avaliações úteis positivas",
        "5 categorias com maior média de avaliações úteis positivas",
        "10 clientes que mais fizeram comentários por grupo"
    ]
    print(MENU)
    while True:
        try:
            opt = int(input('\nChoose an option:\n'))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if opt == 0:
            break
        if 1 <= opt <= 7:
            stmt = stmts[opt - 1]

            if opt <= 3:
                stmt = re.sub(r"pasin = '\w*'",
                              f"pasin = '{args.product_asin}'", stmt)

            print(f"\n=== {query_titles[opt-1]} ===")

            df = pd.read_sql(stmt, engine)

            print(f"Total registers: {len(df)}")
            print("\nResults:")
            print(df)

            csv_path = f'{args.output}/{csv_filenames[opt-1]}'
            df.to_csv(csv_path, index=False)
            print(f"\nResults saved in: {csv_path}")

        else:
            print('Invalid option! Please try again.')


if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)
