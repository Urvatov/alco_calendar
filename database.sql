
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

CREATE TABLE IF NOT EXISTS user
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname TEXT NOT NULL,
    psw TEXT NOT NULL
);



CREATE TABLE IF NOT EXISTS events
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    drink_id INTEGER,
    drink_title TEXT,
    title TEXT,
    event_date DATE NOT NULL,
    volume INTEGER,
    money_spent INTEGER,
    descript TEXT,

    FOREIGN KEY(user_id) REFERENCES user(id) ON UPDATE CASCADE,
    FOREIGN KEY (drink_title) REFERENCES drink(title) ON UPDATE CASCADE,
    FOREIGN KEY(drink_id) REFERENCES drink(id) ON UPDATE CASCADE
);

