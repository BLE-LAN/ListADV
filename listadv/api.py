from flask import (
    Blueprint, request, jsonify
)

from flask_jwt_extended import (
    get_jwt_identity, jwt_required, create_access_token
)

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
