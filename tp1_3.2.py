import os
import re
import csv
import psycopg2 as pg

TXT = "amazon-meta.txt"
with open("schema.sql") as f:
    SQL = f.read()
tables = re.findall(r"(\w+) \(\n", SQL)
PK = {table: set() for table in tables}
TUPS = {table: [] for table in tables}


def nextln(count=1) -> str:
    return re.sub(r"\w+( \w+)?:", "", next(txt), count=count).strip()


def process_product() -> None:
    next(txt)
    pid = nextln()
    pasin = nextln()
    PK["products"].add(pasin)
    title = nextln().replace('"', '""')

    if "discontinued" in title:
        TUPS["products"].append((pid, pasin, "", "", "", "", "", "", "", ""))
        return

    grp = nextln()
    srank = nextln()
    sims, *asins = nextln().split()

    for sim in asins:
        TUPS["similars"].append((pasin, sim))

    cats = nextln()

    for _ in range(int(cats)):
        super_id = ""
        for descr, cid in re.findall(r"\|([^\[]*)\[(\d+)\]", next(txt)):
            if cid not in PK["categories"]:
                PK["categories"].add(cid)
                TUPS["categories"].append((cid, descr, super_id))
            if (pasin, cid) not in PK["products_categories"]:
                PK["products_categories"].add((pasin, cid))
                TUPS["products_categories"].append((pasin, cid))
            super_id = cid

    rev = nextln(0).split()

    for _ in range(int(rev[1])):
        rid = len(TUPS["reviews"])
        TUPS["reviews"].append((rid, pasin, *nextln(0).split()))

    TUPS["products"].append((pid, pasin, title, grp, srank, sims, cats, *rev))


with open(TXT) as txt:
    try:
        next(txt)
        next(txt)
        while True:
            process_product()
    except StopIteration:
        pass

TUPS["similars"] = [t for t in TUPS["similars"] if t[1] in PK["products"]]

os.system("dropdb ecommerce")
os.system("createdb ecommerce")

with pg.connect(
    dbname="ecommerce",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
) as conn:
    with conn.cursor() as curs:
        curs.execute(SQL)
        for table, tups in TUPS.items():
            with open(table, "w") as f:
                csv.writer(f).writerows(tups)
            with open(table) as f:
                curs.copy_expert(f"COPY {table} FROM STDIN WITH CSV", f)
            os.remove(table)
    conn.commit()
