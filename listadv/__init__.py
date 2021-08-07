import os

from datetime import timedelta

from flask import (
    Flask, render_template, make_response
)

from flask_jwt_extended import JWTManager

jwt_ptr = JWTManager()

def create_app(test_config=None):
    
    ACCESS_EXPIRES = timedelta(seconds=600*10)
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'listadv.sqlite'),
        JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES,
        PAGE_SIZE = 2
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
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import mapa
    app.register_blueprint(mapa.bp)

    from . import api
    app.register_blueprint(api.bp)
    
    app.add_url_rule('/', endpoint='index')


    jwt_ptr.init_app(app)

    return app