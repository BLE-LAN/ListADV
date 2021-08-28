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

'''
    TODO REFACTOR 
    This code is too wired, but before remove this need refactor JSON schema and 
    for the moment dont have time to update the Parser and then refactor this app.
'''
def updateDevice(id, adv):
    db = get_db()

    print(id)
    print(adv)

    # Add new datatype
    device_datatype_cursor = db.execute(
        'SELECT type, raw FROM datatype WHERE device = ?', (id,)
    ).fetchall()

    datatypes_dic = {
        'completename' : '',
        'uuids' : ''
    }

    # TODO REFACTOR 
    row = db.execute(
        'SELECT type, raw FROM datatype WHERE device = ? AND type = ?', (id, 'completename')
    ).fetchone()
    if not row and 'completename' in adv:
        insertDataType(id, 'completename', adv['completename'])

    row = db.execute(
        'SELECT type, raw FROM datatype WHERE device = ? AND type = ?', (id, 'uuids')
    ).fetchone()
    if not row and 'uuids' in adv:
        insertDataType(id, 'uuids', adv['uuids'])


    for adv_data in adv['unknowns']:

        data_is_inserted = False
        for device_data in device_datatype_cursor:
            if adv_data['type'] == device_data['type']:
                data_is_inserted = True
                break

        if not data_is_inserted:
            insertDataType(id, adv_data['type'], adv_data['raw'])
                    

    db.execute(
        'UPDATE device' 
        ' SET rssi = ?, timestamp = ?, advtype = ?'
        ' WHERE id = ?',
        (adv['rssi'], adv['timestamp'], adv['advtype'], id)
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

def countAllDevices():
    db = get_db()
    cursor = db.execute('SELECT COUNT(*) FROM device').fetchone()
    return cursor[0]

def getDevicePage(offset, cantidad):
    db = get_db()

    cursor = db.execute(
        'SELECT id, address, advtype, rssi, timestamp '
        'FROM device '
        'ORDER BY rssi DESC '
        'LIMIT ?, ?',
        (offset, cantidad)
    )

    return cursor.fetchall()

def getDeviceAddress(id):
    db = get_db()

    row = db.execute(
        'SELECT address FROM device WHERE id = ?', (id,)
    ).fetchone()

    if row is not None:
        return row['address']
    else:
        return None
    

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

def getDataTypeByDeviceID(device_id):
    db = get_db()

    cursor = db.execute(
        'SELECT * FROM datatype WHERE device = ?', (device_id,)
    )

    datatypes = cursor.fetchall()
    return datatypes