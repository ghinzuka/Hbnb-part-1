CREATE DATABASE IF NOT EXISTS hbnb;

USE hbnb;

CREATE TABLE PlaceAmenity (
    place_id VARCHAR(36),
    amenity_id VARCHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);
