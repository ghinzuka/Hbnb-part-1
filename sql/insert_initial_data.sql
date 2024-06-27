USE hbnb;

INSERT INTO Country (code, name) VALUES ('US', 'United States');
INSERT INTO Country (code, name) VALUES ('FR', 'France');

INSERT INTO City (id, name, country_code) VALUES ('1', 'New York', 'US');
INSERT INTO City (id, name, country_code) VALUES ('2', 'Paris', 'FR');

INSERT INTO User (id, email, password, is_admin) VALUES ('1', 'admin@example.com', 'password', true);
