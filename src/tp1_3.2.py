import argparse
import csv
import math
import os
import re
import time
from dotenv import load_dotenv
import psycopg2 as pg

load_dotenv()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Load SNAP Amazon data into PostgreSQL database')
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
    parser.add_argument('--input', default='../data/snap_amazon.txt',
                        help='Path to SNAP Amazon data file (default: ../data/snap_amazon.txt)')
    return parser.parse_args()


args = parse_arguments()

with open('/app/sql/schema.sql') as f:
    SCHEMA = f.read()
tables = re.findall(r'(\w+) \(\n', SCHEMA)
PK = {table: set() for table in tables}
ROWS = {table: [] for table in tables}


def nextln(n: int = 1) -> str:
    return re.sub(r'\w+( \w+)?:', '', next(txt), count=n).strip()


def process_product() -> None:
    while next(txt).strip():
        continue
    pid = nextln()
    pasin = nextln()
    PK['products'].add(pasin)
    title = nextln().replace('"', '""')

    if 'discontinued' in title:
        ROWS['products'].append((pid, pasin, *['']*8))
        return

    grp = nextln()
    srank = nextln()
    sims, *asins = nextln().split()

    for sim in asins:
        ROWS['similars'].append((pasin, sim))

    cats = nextln()

    for _ in range(int(cats)):
        super_id = ''
        for descr, cid in re.findall(r'\|([^\[]*)\[(\d+)\]', next(txt)):
            if cid not in PK['categories']:
                PK['categories'].add(cid)
                ROWS['categories'].append((cid, descr, super_id))
            super_id = cid
        ROWS['products_categories'].append((pasin, super_id))

    rev = nextln(0).split()

    for _ in range(int(rev[1])):
        rid = len(ROWS['reviews'])
        ROWS['reviews'].append((rid, pasin, *nextln(0).split()))

    ROWS['products'].append((pid, pasin, title, grp, srank, sims, cats, *rev))


def get_time() -> str:
    cur_time = time.time()
    seconds = math.ceil(cur_time - start)
    return f'{seconds // 60}:{seconds % 60:02}'


def populate_db(curs) -> tuple[int, int]:
    inserted = total = 0

    for table, rows in ROWS.items():
        print(f'Creating temporary csv {table}...', end='\r')

        with open(table, 'w') as f:
            csv.writer(f).writerows(rows)

        with open(table) as f:
            curs.copy_expert(f'COPY {table} FROM STDIN WITH CSV', f)

        frac = f'{curs.rowcount:9,} / {len(rows):<9,}'
        print(f'({get_time()}) {frac} rows inserted into {table}')
        total += len(rows)
        inserted += curs.rowcount
        os.remove(table)

    return inserted, total


def main():
    try:
        print('Processing products...', end='\r')
        while True:
            process_product()
    except StopIteration:
        pass

    ROWS['similars'] = [t for t in ROWS['similars'] if t[1] in PK['products']]

    with pg.connect(
        dbname=args.db_name,
        user=args.db_user,
        password=args.db_pass,
        host=args.db_host,
        port=args.db_port
    ) as conn:
        with conn.cursor() as curs:
            curs.execute(SCHEMA)
            inserted, total = populate_db(curs)
            print(f'{inserted:,} / {total:,} rows processed successfully')
        conn.commit()


if __name__ == '__main__':
    if not os.path.exists(args.input):
        print(f'Input file {args.input} not found, downloading from SNAP...')
        os.system(f'cp ../data/amazon-meta.txt.gz {args.input}.gz')
        os.system(f'gunzip {args.input}.gz')
    start = time.time()
    with open(args.input) as txt:
        main()
