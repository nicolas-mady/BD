import os
import re
import csv
import psycopg2 as pg

TXT = "amazon-meta.txt"
SQL = """
CREATE TABLE products (
	pid int PRIMARY KEY,
	asin char(10) UNIQUE NOT NULL,
	title text,
	grp varchar(12),
	srank int,
	sims int,
	cats int,
	tot int,
	dl int,
	av_rt real
);

CREATE TABLE similars (
	asin char(10) REFERENCES products(asin) ON DELETE CASCADE,
	sim char(10) REFERENCES products(asin) ON DELETE CASCADE,
	PRIMARY KEY (asin, sim)
);

CREATE TABLE categories (
	cid int PRIMARY KEY,
	descr text,
	super_id int REFERENCES categories(cid) ON DELETE CASCADE
);

CREATE TABLE products_categories (
	asin char(10) REFERENCES products(asin) ON DELETE CASCADE,
	cid int REFERENCES categories(cid) ON DELETE CASCADE,
	PRIMARY KEY (asin, cid)
);

CREATE TABLE reviews (
	rid int PRIMARY KEY,
	asin char(10) REFERENCES products(asin) ON DELETE CASCADE,
	day date,
	uid varchar(14),
	rating int,
	votes int,
	helpful int
);
"""
tables = re.findall(r"(\w+) \(\n", SQL)
PK = {table: set() for table in tables}
TUPS = {table: [] for table in tables}

def nextln(count=1) -> str:
	return re.sub(r"\w+( \w+)?:", "", next(txt), count=count).strip()


def parse_block():
	next(txt)
	pid = nextln()
	asin = nextln()
	PK["products"].add(asin)
	title = nextln().replace('"', '""')

	if "discontinued" in title:
		TUPS["products"].append((pid, asin, "", "", "", "", "", "", "", ""))
		return

	grp = nextln()
	srank = nextln()
	sims, *asins = nextln().split()

	for sim in asins:
		TUPS["similars"].append((asin, sim))

	cats = nextln()

	for _ in range(int(cats)):
		super_id = ""
		for descr, cid in re.findall(r"\|([^\[]*)\[(\d+)\]", next(txt)):
			if cid not in PK["categories"]:
				PK["categories"].add(cid)
				TUPS["categories"].append((cid, descr, super_id))
			if (asin, cid) not in PK["products_categories"]:
				PK["products_categories"].add((asin, cid))
				TUPS["products_categories"].append((asin, cid))
			super_id = cid

	rev = nextln(0).split()

	TUPS["products"].append((pid, asin, title, grp, srank, sims, cats, *rev))

	for _ in range(int(rev[1])):
		rid = len(TUPS["reviews"])
		TUPS["reviews"].append((rid, asin, *nextln(0).split()))


with open(TXT) as txt:
	try:
		next(txt)
		next(txt)
		while True:
			parse_block()
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
