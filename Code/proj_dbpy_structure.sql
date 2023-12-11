DROP DATABASE if EXISTS proj_dbpy;
CREATE DATABASE if NOT EXISTS proj_dbpy;

USE proj_dbpy;

-- création des utilisateurs
DROP USER if EXISTS 'customer'@'localhost';
DROP USER if EXISTS 'su'@'localhost';
CREATE USER 'customer'@'localhost' IDENTIFIED BY '';
GRANT INSERT, SELECT ON proj_dbpy.* TO 'customer'@'localhost';
CREATE USER 'su'@'localhost' IDENTIFIED BY 'changeme';
GRANT INSERT, SELECT, DELETE ON proj_dbpy.* TO 'su'@'localhost';

-- création de la table parties
DROP TABLE if EXISTS parties;
CREATE TABLE if NOT EXISTS parties (
	id INT NOT NULL AUTO_INCREMENT,
	Pseudo VARCHAR(45) NOT NULL,
	game VARCHAR(45) NOT NULL,
	nb_ok INT NOT NULL,
	nb_Total INT NOT NULL,
	start_date DATE NOT NULL,
	total_time TIME NOT NULL,
	PRIMARY KEY (id));