from flask import Flask
from app.extensions import mongo
from app.webhook.routes import webhook_bp
from app.routes import events_bp

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/webhook_db"
    
    # Initialize extensions
    mongo.init_app(app)
    
    # Register blueprints
    app.register_blueprint(webhook_bp)
    app.register_blueprint(events_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)