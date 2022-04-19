from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from sqlalchemy import true
from earthdaily.api.v1 import atm

db = SQLAlchemy()

def create_app(config=None):

    app = Flask(__name__)
    """ === Flask Configuration === """
    from .configs import DevelopmentConfig, ProductionConfig
    if not config:
        if app.config['DEBUG']:
            config = DevelopmentConfig()
        else:
            config = ProductionConfig()
        
        app.config.from_object(config)

    db.init_app(app)

    api = Api(
        app, 
        doc='/docs',
        version='1.0', 
        title='ATM API',
        description='ATM Api for assignment',
    )

    api.add_namespace(atm.ns)

    @app.errorhandler(404)
    def page_404(error):
        return '404 not founded', 404

    @app.before_request   
    def before_request():
        g.db = db.session

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'db'):
            g.db.close()
    return app

