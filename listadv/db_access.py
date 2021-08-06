import sqlite3
import click

from listadv.db import get_db


''''
    utilities functions
'''

def lastInsertRowId():
    db = get_db()
    rowid = db.execute('SELECT last_insert_rowid()')
    return rowid.lastrowid


'''
    user table
'''

def getTokenByUsername(username):
    db = get_db()

    row = db.execute(
		'SELECT token FROM user WHERE username = ?', (username,)
	).fetchone()

    return row['token']


def setTokenByUsername(token, username):
    db = get_db()

    db.execute(
        'UPDATE user SET token = ? WHERE username = ?',
        (token, username)
    )
    
    db.commit()

def updateUserToken(newToken, oldToken):
    db = get_db()

    db.execute(
		'UPDATE user SET token = ? WHERE token = ?',
		(newToken, oldToken)
	)

    db.commit()


'''
    device table
'''

def getDeviceIdByAddress(address):
    db = get_db()

    row = db.execute(
        'SELECT id FROM device WHERE address = ?', (address,)
    ).fetchone()

    if row is not None:
        return row['id']
    else:
        return None

def updateDevice(id, rssi, timestamp):
    db = get_db()

    db.execute(
        'UPDATE device' 
        ' SET rssi = ?, timestamp = ?'
        ' WHERE id = ?',
        (rssi, timestamp, id)
    )

    db.commit()

def insertDevice(address, advtype, rssi, timestamp):
    db = get_db()

    db.execute(
        'INSERT INTO device (address, advtype, rssi, timestamp)'
        ' VALUES (?, ?, ?, ?)', 
        (address, advtype, rssi, timestamp)
    )

    db.commit()


'''
    datatype table
'''

def insertDataType(device, tipo, raw):
    db = get_db()

    db.execute(
        'INSERT INTO datatype (device, type, raw)'
        ' VALUES (?, ?, ?)', 
        (device, tipo, raw)
    )

    db.commit()