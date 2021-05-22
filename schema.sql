CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT,
    password TEXT,
    admin BOOL DEFAULT false
);

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    location TEXT,
    user_id INTEGER REFERENCES users,
    added_at TIMESTAMP
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    user_id INTEGER REFERENCES users,
    restaurant_id INTEGER REFERENCES restaurants,
    sent_at TIMESTAMP
);