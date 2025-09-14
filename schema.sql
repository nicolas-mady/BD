DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS similars CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS products_categories CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;

CREATE TABLE products (
	pid int PRIMARY KEY,
	pasin char(10) UNIQUE NOT NULL,
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
	pasin char(10) REFERENCES products(pasin) ON DELETE CASCADE,
	sim char(10) REFERENCES products(pasin) ON DELETE CASCADE,
	PRIMARY KEY (pasin, sim)
);

CREATE TABLE categories (
	cid int PRIMARY KEY,
	descr text,
	super_id int REFERENCES categories(cid) ON DELETE CASCADE
);

CREATE TABLE products_categories (
	pasin char(10) REFERENCES products(pasin) ON DELETE CASCADE,
	cid int REFERENCES categories(cid) ON DELETE CASCADE,
	PRIMARY KEY (pasin, cid)
);

CREATE TABLE reviews (
	rid int PRIMARY KEY,
	pasin char(10) REFERENCES products(pasin) ON DELETE CASCADE NOT NULL,
	rdate date NOT NULL,
	usr_id varchar(14) NOT NULL,
	rating int NOT NULL,
	votes int NOT NULL,
	helpful int NOT NULL
);
