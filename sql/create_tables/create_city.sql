CREATE DATABASE IF NOT EXISTS hbnb;

USE hbnb;

CREATE TABLE City (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    country_code VARCHAR(2),
    FOREIGN KEY (country_code) REFERENCES Country(code)
);
