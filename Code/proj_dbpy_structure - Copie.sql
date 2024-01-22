DROP DATABASE if EXISTS proj_dbpy;
CREATE DATABASE if NOT EXISTS proj_dbpy;

USE proj_dbpy;

-- création des utilisateurs
DROP USER if EXISTS 'customer'@'localhost';
DROP USER if EXISTS 'su'@'localhost';
CREATE USER 'customer'@'localhost' IDENTIFIED BY '';
CREATE USER 'su'@'localhost' IDENTIFIED BY 'changeme';

-- création de la table parties
DROP TABLE if EXISTS parties;
CREATE TABLE if NOT EXISTS parties (
	id INT NOT NULL AUTO_INCREMENT,
	Pseudo VARCHAR(45) NOT NULL,
	game VARCHAR(45) NOT NULL,
	nb_ok INT NOT NULL,
	nb_Total INT NOT NULL,
	start_date DATE NOT NULL,
	`time` TIME NOT NULL,
	PRIMARY KEY (id));

DROP TABLE if EXISTS users;
CREATE TABLE if NOT EXISTS users (
	id INT NOT NULL AUTO_INCREMENT,
	Pseudo VARCHAR(45) NOT NULL,
	userType VARCHAR(45) NOT NULL,
	passwd VARCHAR(450),
	PRIMARY KEY (id));

# ajouter les droits aux utilisateurs	
GRANT INSERT, SELECT ON proj_dbpy.* TO 'customer'@'localhost';
GRANT ALL ON proj_dbpy.* TO 'su'@'localhost';

INSERT INTO users (Pseudo, userType)
VALUES ("su", "admin")