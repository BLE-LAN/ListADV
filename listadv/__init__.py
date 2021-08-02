import os

from flask import Flask
from flask import render_template
from flask import make_response

from flask_jwt_extended import JWTManager

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

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.errorhandler(404)
    def page_not_found(error):
        resp = make_response(render_template('404.html'), 404)
        resp.headers['X-Something'] = 'A value'
        return resp

    jwt = JWTManager()
    jwt.init_app(app)
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import mapa
    app.register_blueprint(mapa.bp)

    from . import api
    app.register_blueprint(api.bp)
    
    app.add_url_rule('/', endpoint='index')

    return app