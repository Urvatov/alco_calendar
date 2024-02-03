CREATE TABLE IF NOT EXISTS user
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname TEXT NOT NULL,
    psw TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS drink 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price INTEGER NOT NULL,
    alcohol INTEGER NOT NULL,
    volume REAL NOT NULL,

    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS events
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    event_date DATE NOT NULL,
    place TEXT,
    descript TEXT,
    FOREIGN KEY(user_id) REFERENCES user(id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS events_drink
(
    id INTEGER,
    user_id INTEGER,
    event_id INTEGER,
    drink_id INTEGER,
    drink_title TEXT,
    drink_alcohol REAL,
    volume INTEGER,
    price INTEGER,

    PRIMARY KEY(id)
    
    FOREIGN KEY(user_id) REFERENCES user(id) ON UPDATE CASCADE,
    FOREIGN KEY(event_id) REFERENCES events(id) ON UPDATE CASCADE,
    FOREIGN KEY(drink_id) REFERENCES drink(id) ON UPDATE CASCADE,
    FOREIGN KEY(drink_alcohol) REFERENCES drink(alcohol) ON UPDATE CASCADE
);
