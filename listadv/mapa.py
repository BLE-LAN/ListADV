from flask import (
    Blueprint, render_template, session, redirect, url_for, request, jsonify, current_app
)

from werkzeug.exceptions import abort

from listadv.auth import login_required
from listadv.db import get_db
from listadv.db_access import *

bp = Blueprint('mapa', __name__, url_prefix='/mapa')

@bp.route('/lista', methods=['GET'])
def lista():
    if session.get('user_id') is None:
        return redirect(url_for('auth.login'))

    PAGE_SIZE = current_app.config['PAGE_SIZE']

    total_records = countAllDevices()

    num_paginas = (total_records // PAGE_SIZE)

    if (total_records % PAGE_SIZE) > 0:
        num_paginas += 1

    devices = getDevicePage(0, PAGE_SIZE)

    return render_template('mapa/basetable.html', devices=devices, num_paginas=num_paginas, actual=1)

@bp.route('/lista/pagina/<int:pagina>', methods=['GET', 'POST'])
def pagina(pagina=None):
    total_records = countAllDevices()

    PAGE_SIZE = current_app.config['PAGE_SIZE']

    num_paginas = (total_records // PAGE_SIZE)

    if (total_records % PAGE_SIZE) > 0:
        num_paginas += 1

    if (pagina <= 0) or (pagina > num_paginas):
        pagina = 1

    offset = PAGE_SIZE * (pagina - 1)

    devices = getDevicePage(offset, PAGE_SIZE)

    return render_template('mapa/lista.html', devices=devices, num_paginas=num_paginas, actual=pagina)

@bp.route('/lista/detalle/<int:device>', methods=['GET', 'POST'])
def detalle(device=None):
    datatypes = getDataTypeByDeviceID(device)
    address = getDeviceAddress(device)
    return render_template('mapa/datatypes.html', datatypes=datatypes, address=address)