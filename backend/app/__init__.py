from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from app.routes import register_routes
from app.config import Config

def create_app():
    
    app = Flask(__name__)
    
    app.config.from_object(Config)

    CORS(app)
    
    api = Api(app)
    
    register_routes(api)
    
    return app