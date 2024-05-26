from pathlib import Path
from flask import Flask
from . import control

def create_app():
    
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)
    
    # Ensure that instance folder exists
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(control.bp)
    
    # Hello
    @app.route('/hello')
    def hello():
        return 'Hello world!'
    
    return app