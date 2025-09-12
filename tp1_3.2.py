import os
import re
import csv
import psycopg2 as pg

TXT = "amazon-meta-sample.txt"
SQL = """
CREATE TABLE IF NOT EXISTS product (
    id int UNIQUE NOT NULL,
    asin char(10) PRIMARY KEY,
    title text,
    pgroup varchar(12),
    salesrank int,
    sim int,
    cats int,
    tot int,
    dl int,
    avg_rating real
);

CREATE TABLE IF NOT EXISTS psimilar (
    asin char(10) REFERENCES product(asin) ON DELETE CASCADE,
    asin_sim char(10) REFERENCES product(asin) ON DELETE CASCADE,
    PRIMARY KEY (asin, asin_sim)
);

CREATE TABLE IF NOT EXISTS category (
    cat_id int PRIMARY KEY,
    descr text
);

CREATE TABLE IF NOT EXISTS product_category (
    asin char(10) REFERENCES product(asin) ON DELETE CASCADE,
    cat_id int REFERENCES category(cat_id) ON DELETE CASCADE,
    PRIMARY KEY (asin, cat_id)
);

CREATE TABLE IF NOT EXISTS category_hierarchy (
    cat_id int REFERENCES category(cat_id) ON DELETE CASCADE,
    parent_id int REFERENCES category(cat_id) ON DELETE CASCADE,
    PRIMARY KEY (cat_id, parent_id)
);

CREATE TABLE IF NOT EXISTS review (
    asin char(10) REFERENCES product(asin) ON DELETE CASCADE,
    rdate date NOT NULL,
    usr_id varchar(14),
    rating int NOT NULL,
    votes int NOT NULL,
    helpful int NOT NULL,
    PRIMARY KEY (asin, usr_id, rdate)
);
"""
TUPS = {table: set() for table in re.findall(r"(\w+) \(\n", SQL)}


def nextln(count=1) -> str:
    return re.sub(r"\w+:", "", next(txt), count=count).strip()


def parse_block():
    nextln()
    id_ = nextln()
    asin = nextln()
    title = nextln().replace('"', '""')
    if "discontinued" in title:
        TUPS["product"].add((id_, asin, "", "", "", "", "", "", "", ""))
        return
    pgroup = nextln()
    salesrank = nextln()
    sim, *asins = nextln().split()
    for asin_sim in asins:
        TUPS["psimilar"].add((asin, asin_sim))
    cats = nextln()
    for _ in range(int(cats)):
        parent_id = None
        for descr, cat_id in re.findall(r"\|([^\[]*)\[(\d+)\]", next(txt)):
            parent_id = parent_id or cat_id
            TUPS["category"].add((cat_id, descr))
            TUPS["product_category"].add((asin, cat_id))
            TUPS["category_hierarchy"].add((cat_id, parent_id))
            parent_id = cat_id
    tot, dl, _, avg_rating = nextln(0).split()
    TUPS["product"].add(
        (id_, asin, title, pgroup, salesrank, sim, cats, tot, dl, avg_rating)
    )
    for _ in range(int(dl)):
        TUPS["review"].add((asin, *nextln(0).split()))


def populate():
    curs.execute(SQL)
    for table, tups in TUPS.items():
        file = f"{table}.csv"
        with open(file, "w") as f:
            csv.writer(f).writerows(tups)
        with open(file) as f:
            curs.copy_expert(f"COPY {table} FROM STDIN WITH CSV", f)
        # os.remove(file)


with open(TXT) as txt:
    next(txt)
    next(txt)
    try:
        while True:
            parse_block()
    except StopIteration:
        pass

asins = {p[1] for p in TUPS["product"]}
TUPS["psimilar"] = {s for s in TUPS["psimilar"] if s[1] in asins}

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
        populate()
    conn.commit()
