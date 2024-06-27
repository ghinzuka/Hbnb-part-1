CREATE DATABASE IF NOT EXISTS hbnb;

USE hbnb;

CREATE TABLE Place (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    description TEXT NOT NULL,
    address VARCHAR(255) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    host_id VARCHAR(36),
    city_id VARCHAR(36),
    price_per_night INT NOT NULL,
    number_of_rooms INT NOT NULL,
    number_of_bathrooms INT NOT NULL,
    max_guests INT NOT NULL,
    FOREIGN KEY (host_id) REFERENCES User(id),
    FOREIGN KEY (city_id) REFERENCES City(id)
);
