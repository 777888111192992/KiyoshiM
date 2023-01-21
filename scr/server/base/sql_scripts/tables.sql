CREATE TABLE post(
    id INTEGER PRIMARY KEY,
    post VARCHAR(100) NOT NULL
);

CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    power_level INT NOT NULL
);

CREATE TABLE personnel(
    id INTEGER PRIMARY KEY,
    surname VARCHAR(100) NOT NULL,
    post_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    patronymic VARCHAR(100) NOT NULL,
    date_birth VARCHAR(100) NOT NULL UNIQUE,
    FOREIGN KEY(post_id) REFERENCES post(id)
);

CREATE TABLE zoo(
    id INTEGER PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    phone VARCHAR(100) NOT NULL,
    city_id INT NOT NULL,
    price INT NOT NULL,
    FOREIGN KEY (city_id)
        REFERENCES cities(id)
        ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE cities(
    id INTEGER PRIMARY KEY,
    title VARCHAR(100) NOT NULL
);

CREATE TABLE animals(
    id INTEGER PRIMARY KEY,
    homeland_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    zoo_id INTEGER NOT NULL,
    tickets_id INTEGER NOT NULL,
    nickname VARCHAR(100) NOT NULL,
    average_life_expectancy VARCHAR(100) NOT NULL,
    FOREIGN KEY(homeland_id) REFERENCES homeland(id)
                  ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY(class_id) REFERENCES class(id)
                  ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY(zoo_id) REFERENCES zoo(id)
                  ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY(tickets_id) REFERENCES tickets(id)
                  ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE class(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE homeland(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE tickets(
    id INTEGER PRIMARY KEY,
    zoo_id INT NOT NULL,
    user_id INT NOT NULL,
    date VARCHAR(255) NOT NULL,
    FOREIGN KEY (zoo_id)
        REFERENCES zoo(id)
        ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE ON UPDATE NO ACTION

);