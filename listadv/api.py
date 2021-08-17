from flask import (
	Blueprint, request, jsonify, current_app
)

from flask_jwt_extended import (
	get_jwt_identity, jwt_required, create_access_token
)

# jwt_ptr es un JWTManager instanciado en __init__
from . import (
	auth, jwt_ptr 
)

from listadv.util import data_type_value_to_description

from listadv.db import get_db
from listadv import util
from listadv.db_access import *

from flask_expects_json import expects_json


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/login', methods=['POST'])
def login():
	if request.json is None:
		return jsonify("No JSON data"), 400
	
	username = request.json.get("username", None)
	password = request.json.get("password", None)

	error = auth.checklogin(username, password)
	
	if error is not None:
		return jsonify("Wrong username or password"), 401
	
	db = get_db()
	
	usertoken = getTokenByUsername(username)
	
	if usertoken is None:
		token = create_access_token(identity=username)
		setTokenByUsername(token, username)
		return jsonify(access_token=token)
	
	return jsonify(access_token=usertoken)


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

	updates = 0
	news = 0

	for device in devices:

		deviceId = getDeviceIdByAddress(device['address'])

		if deviceId is not None:
			updateDevice(deviceId, device['rssi'], device['timestamp'])
			updates += 1
		else:
			news += 1
			insertDevice(device['address'], device['advtype'], device['rssi'], device['timestamp'])

			deviceID = lastInsertRowId()

			# Insertar tipos desconocidos (dados en raw)
			if 'unknowns' in device:
				for unkown in device['unknowns']:
					insertDataType(
						deviceID, 
						data_type_value_to_description(unkown['type']), 
						unkown['raw'])

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
					insertDataType(deviceID, key, value)

	return jsonify(added=news, updated=updates)

@jwt_ptr.expired_token_loader
def remove_expired_token(jwt_header, jwt_payload):
	token = util.encode_jwt(jwt_header, jwt_payload)
	updateUserToken(None, token)
	return jsonify("Token has expired"), 401
