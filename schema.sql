DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS drinks CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS stores CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category TEXT
);

CREATE TABLE drinks (
    id SERIAL PRIMARY KEY,
    name TEXT,
    percentage TEXT,
    category_id TEXT,
    store_ids TEXT,
    price TEXT
);

CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    drink_id INTEGER,
    user_id INTEGER,
    review TEXT,
    score INTEGER
);

INSERT INTO stores (name)
VALUES ('Alko'), 
('Lidl'), 
('S-ryhmä'), 
('K-ryhmä'), 
('R-kioski');

INSERT INTO categories (category)
VALUES ('Beer'), 
('Long drink'), 
('Cider'), 
('Hard seltzer'), 
('Wine'), 
('Liqueur'), 
('Spirit'), 
('Other');