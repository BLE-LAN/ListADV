
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


data_value_description_dict = {
    0x01 : 'Flags',

    0x02 : 'UUIDs 16-bit avaliable',
    0x03 : 'UUIDs 16-bit complete avaliable',
    0x04 : 'UUIDs 32-bit avaliable',
    0x05 : 'UUIDs 32-bit complete avaliable',
    0x06 : 'UUIDs 128-bit avaliable',
    0x07 : 'UUIDs 128-bit complete avaliable',

    0x08 : 'Shortened local name',
    0x09 : 'Complete local name',

    0xA : 'TX Power Level',

    0xD : 'Class of device',
    0xE : 'Pairing Hash',
    0xF : 'Pairing Randomizer',
    
    0x10 : 'TK Value',

    0x11 : 'OOB Flags',

    0x12 : 'Slave Connection Interval',

    0x14 : '16-bit Service UUIDs',
    0x15 : '128-bit Service UUIDs',

    0x16 : 'Service Data',

    0xFF : 'Manufacturer Specific Data'
}


def data_type_value_to_description(value):
    integer_value = int(value, base=16)
    if (integer_value in data_value_description_dict) == False:
        return value

    return data_value_description_dict[int(value, base=16)]

