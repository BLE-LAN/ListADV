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

INSERT INTO device as d (address, advtype, rssi, timestamp) VALUES ('C1:BB:C2:C9:71:1E', 'ConnectableUndirected', -56, 'Tue Jul 27 10:15:20 2021');
INSERT INTO device as d (address, advtype, rssi, timestamp) VALUES ('C1:BB:C2:C9:71:2E', 'ConnectableUndirected', -56, 'Tue Jul 27 10:15:20 2021');
INSERT INTO device as d (address, advtype, rssi, timestamp) VALUES ('C1:BB:C2:C9:71:3E', 'ConnectableUndirected', -56, 'Tue Jul 27 10:15:20 2021');
INSERT INTO device as d (address, advtype, rssi, timestamp) VALUES ('C1:BB:C2:C9:71:4E', 'ConnectableUndirected', -56, 'Tue Jul 27 10:15:20 2021');
INSERT INTO device as d (address, advtype, rssi, timestamp) VALUES ('C1:BB:C2:C9:71:5E', 'ConnectableUndirected', -56, 'Tue Jul 27 10:15:20 2021');
INSERT INTO device as d (address, advtype, rssi, timestamp) VALUES ('C1:BB:C2:C9:71:6E', 'ConnectableUndirected', -56, 'Tue Jul 27 10:15:20 2021');

INSERT INTO datatype (device, type, raw) VALUES (1, 'completename', 'best nombre para un BLE: uwu');
