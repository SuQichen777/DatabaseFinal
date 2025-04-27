DROP TABLE IF EXISTS testIdentity;
CREATE TABLE testIdentity (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);
INSERT INTO testIdentity (name) VALUES ('John Doe');