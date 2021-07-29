import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'listadv.sqlite'),
        SEND_FILE_MAX_AGE_DEFAULT = 0
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    '''
    @app.route('/hola')
    def hola():
        return 'ie'
    '''
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import mapa
    app.register_blueprint(mapa.bp)
    
    app.add_url_rule('/', endpoint='index')

    return app