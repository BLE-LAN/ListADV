from flask import (
    Blueprint, flash, g, request, session, url_for, current_app
)

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token

from flask import jsonify

from listadv.db import get_db

from . import auth

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        error = auth.checklogin(username, password)
        
        if error is None:
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token)

    return jsonify("Wrong username or password"), 401

@bp.route('/adddevices', methods=('GET', 'POST'))
@jwt_required()
def adddevices():
    return "hola"
