DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS datatypes;
DROP TABLE IF EXISTS user;

CREATE TABLE devices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  address TEXT UNIQUE NOT NULL,
  advtype TEXT NOT NULL,
  rssi INTEGER NOT NULL,
  timestamp TEXT NOT NULL
);

CREATE TABLE datatypes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type INTEGER NOT NULL, 
  raw TEXT NOT NULL,
  FOREIGN KEY (id) REFERENCES devices (id)
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  token TEXT UNIQUE
);

INSERT INTO devices as d (address, advtype, rssi, timestamp) VALUES ('C1:BB:C2:C9:71:5E', 'ConnectableUndirected', -56, 'Tue Jul 27 10:15:20 2021')