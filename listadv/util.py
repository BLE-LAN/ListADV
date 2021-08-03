
import jwt

from flask import current_app

def access_token_get_jti(access_token):
    payload = jwt.decode(
        access_token, 
        current_app.config['SECRET_KEY'], 
        algorithms="HS256"
    )
    return payload['jti']

def encode_jwt(header, payload):
    return jwt.encode(
        payload, 
        current_app.config['SECRET_KEY'], 
        algorithm="HS256",
        headers=header
    )