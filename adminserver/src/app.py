import logging.config
from quart import Quart, g
from quart_schema import QuartSchema
# Imports from within the project
import config as cfg
from src.api.v1.routes import api_v1_bp
from src.auth.routes import auth_bp
from src.db import AsyncSessionLocal, setup_db

# TODO - Add quart-schema and validate request & response data
# TODO - Add blueprints and separate auth into it's own section

def create_app():
    # Instantiate the application
    app = Quart(__name__)
    
    # Logging
    logging.config.dictConfig(cfg.LOG_CONFIG)
    
    # Security
    app.config['SECRET_KEY'] = cfg.APP_SECRET_KEY
    
    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_v1_bp)

    # Schema
    QuartSchema(app, convert_casing=True)
    app.config["QUART_SCHEMA_CONVERSION_PREFERENCE"] = "pydantic"
    
    
    # Database
    @app.before_serving
    async def startup():
        await setup_db()

    @app.before_request
    async def create_session():
        g.db_session = AsyncSessionLocal()

    @app.after_request
    async def cleanup_session(response):
        await g.db_session.close()
        return response

    @app.teardown_request
    async def teardown_session(exc):
        session = getattr(g, "db_session", None)
        if session:
            if exc:
                await session.rollback()
            await session.close()

    return app