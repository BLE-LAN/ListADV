DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS datatype;
DROP TABLE IF EXISTS user;

CREATE TABLE device (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  address TEXT UNIQUE NOT NULL,
  advtype TEXT NOT NULL,
  rssi INTEGER NOT NULL,
  timestamp TEXT NOT NULL
);

CREATE TABLE datatype (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device INTEGER NOT NULL,
  type TEXT NOT NULL, 
  raw TEXT NOT NULL,
  FOREIGN KEY(device) REFERENCES device(id)
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  token TEXT UNIQUE
);
