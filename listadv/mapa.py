from flask import (
    Blueprint, render_template, session, redirect, url_for, request, jsonify
)

from werkzeug.exceptions import abort

from listadv.auth import login_required
from listadv.db import get_db
from listadv.db_access import getDataTypeByDeviceID

bp = Blueprint('mapa', __name__, url_prefix='/mapa')

@bp.route('/lista', methods=('GET', 'POST'))
def lista():
    if session.get('user_id') is not None:
        db = get_db()
        devices = db.execute(
            'SELECT *'
            ' FROM device'
        ).fetchall()
        return render_template('mapa/lista.html', devices=devices)
    else:
        return redirect(url_for('auth.login'))

@bp.route('/lista/detalle/<device>', methods=['POST'])
def detalle(device=None):
    datatypes = getDataTypeByDeviceID(device)
    return render_template('mapa/datatypes.html', datatypes=datatypes)