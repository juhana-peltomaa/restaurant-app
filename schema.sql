CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT,
    password TEXT,
    picture BYTEA,
    admin BOOL DEFAULT false
);

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    location TEXT,
    website TEXT,
    info TEXT,
    user_id INTEGER REFERENCES users,
    added_at TIMESTAMP
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    stars INTEGER,
    writer TEXT,
    user_id INTEGER REFERENCES users,
    restaurant_id INTEGER REFERENCES restaurants ON DELETE CASCADE,
    sent_at TIMESTAMP
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category TEXT,
    category_restaurant_id INTEGER REFERENCES restaurants ON DELETE CASCADE
);

CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    favorite_user_id INTEGER REFERENCES users (id),
    favorite_restaurant_id INTEGER REFERENCES restaurants (id) ON DELETE CASCADE
);