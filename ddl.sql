CREATE DATABASE rewardmeasure;

-- Create the tables
CREATE TABLE users(
   username varchar(20) PRIMARY KEY,
   role varchar(30),
   email varchar(30)
);

CREATE TABLE redemption (
	 username VARCHAR(20),
	 timestamp TIMESTAMP,
     amount INT,
	 PRIMARY KEY (username, timestamp),
	 FOREIGN KEY (username) REFERENCES users(username)
);

CREATE TABLE transaction (
	 sender VARCHAR(20),
	 receiver VARCHAR(20),
	 timestamp TIMESTAMP,
	 amount INT,
	 message VARCHAR(200),
	 PRIMARY KEY (sender, receiver, timestamp),
	 FOREIGN KEY (sender) REFERENCES users(username),
	 FOREIGN KEY (receiver) REFERENCES users(username)
);

CREATE TABLE account (
	 username VARCHAR(20) PRIMARY KEY,
	 to_give INT,
     to_receive INt,
	 to_redeem INT,
	 FOREIGN KEY (username) REFERENCES users(username)
);