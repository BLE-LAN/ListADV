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


@bp.route('/adddevices', methods=('GET', 'POST'))
@jwt_required()
def adddevices():
    return "hola"


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
