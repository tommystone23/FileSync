CREATE DATABASE IF NOT EXISTS filesyncDB;
USE filesyncDB;

CREATE TABLE IF NOT EXISTS users(
	userID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(64),
	pw CHAR(64),
	rootDirectory VARCHAR(64),
	salt VARCHAR(64));

