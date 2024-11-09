DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL
);

INSERT INTO users (email, name) VALUES ("bob@dylan.com", "Bob");
INSERT INTO users (email, name) VALUES ("sylvie@dylan.com", "Sylvie");

-- This insert should fail because of the unique email constraint
INSERT INTO users (email, name) VALUES ("bob@dylan.com", "Jean");

SELECT * FROM users;
