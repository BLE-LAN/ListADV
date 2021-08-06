from flask import (
	Blueprint, request, jsonify, current_app
)

from flask_jwt_extended import (
	get_jwt_identity, jwt_required, create_access_token
)

# jwt es un JWTManager instanciado en __init__
# no se me ha occurido una forma "elegante" de obtenerla
from . import (
		auth, jwt_ptr 
)

from listadv.db import get_db
from . import util

import redis

from flask_expects_json import expects_json



bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/login', methods=['POST'])
def login():
	username = request.json.get("username", None)
	password = request.json.get("password", None)

	error = auth.checklogin(username, password)
	
	if error is not None:
		return jsonify("Wrong username or password"), 401
	
	db = get_db()

	row = db.execute(
		'SELECT token FROM user WHERE username = ?', (username,)
	).fetchone()
	
	if row['token'] is None:
		token = create_access_token(identity=username)

		db.execute(
			'UPDATE user SET token = ? WHERE username = ?',
			(token, username)
		)
		db.commit()
		return jsonify(access_token=token)
	
	return jsonify(access_token=row['token'])

schema = {
	"type": "object",
	"properties": {
		"devices": {
			"type": "array",
			"items": { "$ref": "#/$defs/device" }
		}
	},
	"$defs": {
		"device": {
			"type": "object",
			"required": [ "address", "advtype", "rssi", "timestamp"],
			"properties": {
				"address": {
					"type": "string",
				},
				"advtype": {
					"type": "string",
				},
				"rssi": {
					"type": "integer",
					"maximum": 0
				},
				"timestamp": {
					"type": "string",
				}
			}
		}
	}
}


@bp.route('/adddevices', methods=['POST'])
@jwt_required()
@expects_json(schema)
def adddevices():
	try:
		request_data = request.json
	except NotUniqueError as e:
		return jsonify(dict(message=e.message)), 409
	
	db = get_db()
	devices = request_data['devices']

	for device in devices:
		row = db.execute(
			'SELECT id FROM device WHERE address = ?', (device['address'],)
		).fetchone()

		if row is not None:
			db.execute(
				'UPDATE device' 
				' SET rssi = ?, timestamp = ?'
				' WHERE id = ?',
				(device['rssi'], device['timestamp'], row['id'])
			)
		else:
			db.execute(
				'INSERT INTO device (address, advtype, rssi, timestamp)'
				' VALUES (?, ?, ?, ?)', 
				(device['address'], device['advtype'], device['rssi'], device['timestamp'])
			)

			db.commit()

			deviceId = db.execute(
				'SELECT last_insert_rowid()'
			)

			deviceID = deviceId.lastrowid

			# Insertar tipos desconocidos (dados en raw)
			for unkown in device['unknows']:
				db.execute(
					'INSERT INTO datatype (device, type, raw)'
					' VALUES (?, ?, ?)', 
					(deviceID, unkown['type'], unkown['raw'])
				)

			# Insertar tipos conocidos
			datatypes_dic = {
				'completename' : '',
				'uuids' : ''
			}

			if 'completename' in device:
				datatypes_dic['completename'] = device['completename']

			if 'uuids' in device:
					for uuid in device['uuids']:
						datatypes_dic['uuids'] += uuid + ' '

			for key in datatypes_dic.keys():
				value = datatypes_dic[key]
				if len(value) > 0: 
					db.execute(
						'INSERT INTO datatype (device, type, raw)'
						' VALUES (?, ?, ?)', 
						(deviceID, key, value)
					)

			print(datatypes_dic)

		db.commit()

	return request_data

@jwt_ptr.expired_token_loader
def remove_expired_token(jwt_header, jwt_payload):
	
	token = util.encode_jwt(jwt_header, jwt_payload)
	db = get_db()

	db.execute(
		'UPDATE user SET token = ? WHERE token = ?',
		(None, token)
	)

	db.commit()

	return jsonify("Token has expired"), 401
