import os
import re
import csv
import psycopg2 as pg
import time
import math

TXT = 'amazon-meta.txt'
with open('schema.sql') as sql:
    SQL = sql.read()
tables = re.findall(r'(\w+) \(\n', SQL)
PK = {table: set() for table in tables}
ROWS = {table: [] for table in tables}


def nextln(n: int = 1) -> str:
    return re.sub(r'\w+( \w+)?:', '', next(txt), count=n).strip()


def process_product() -> None:
    next(txt)
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
            # if (pasin, cid) not in PK['products_categories']:
            #     PK['products_categories'].add((pasin, cid))
            #     TUPS['products_categories'].append((pasin, cid))
            super_id = cid
        ROWS['products_categories'].append((pasin, super_id))

    rev = nextln(0).split()

    for _ in range(int(rev[1])):
        rid = len(ROWS['reviews'])
        ROWS['reviews'].append((rid, pasin, *nextln(0).split()))

    ROWS['products'].append((pid, pasin, title, grp, srank, sims, cats, *rev))


def get_time() -> str:
    cur = time.time()
    sec = math.ceil(cur - start)
    return f'{sec // 60}:{sec % 60:02}'


def populate_db() -> tuple[int, int]:
    total = inserted = 0

    for table, rows in ROWS.items():
        print(f'Creating temporary csv {table}...', end='\r')

        with open(table, 'w') as tmp_csv:
            csv.writer(tmp_csv).writerows(rows)

        with open(table) as tmp_csv:
            curs.copy_expert(f'COPY {table} FROM STDIN WITH CSV', tmp_csv)

        print(f'({get_time()}) {curs.rowcount:9,} / {len(rows):<9,} rows inserted into {table}')
        total += len(rows)
        inserted += curs.rowcount
        os.remove(table)

    return total, inserted


start = time.time()

with open(TXT) as txt:
    try:
        next(txt)
        next(txt)
        print('Processing products...', end='\r')
        while True:
            process_product()
    except StopIteration:
        pass

ROWS['similars'] = [t for t in ROWS['similars'] if t[1] in PK['products']]

with pg.connect(
    dbname='ecommerce',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
) as conn:
    with conn.cursor() as curs:
        curs.execute(SQL)
        total, inserted = populate_db()
        print(f'{inserted:,} / {total:,} rows processed')
    conn.commit()
