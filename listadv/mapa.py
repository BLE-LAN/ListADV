from flask import (
    Blueprint, render_template
)

from werkzeug.exceptions import abort

from listadv.auth import login_required
from listadv.db import get_db

bp = Blueprint('mapa', __name__, url_prefix='/mapa')

@bp.route('/lista', methods=('GET', 'POST'))
def lista():
    db = get_db()
    devices = db.execute(
        'SELECT mac, type, rssi'
        ' FROM devices'
    ).fetchall()
    return render_template('mapa/lista.html', devices=devices)