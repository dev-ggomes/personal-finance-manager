from flask import Flask
from source.assets import init_assets
from source.db import engine
from source.models import Base

# Create and configure the Flask app
def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Compile SCSS assets
    init_assets(app)

    # Initialize database schema
    Base.metadata.create_all(engine)

    # Register Blueprints
    from source.views.dashboard import bp as dashboard_bp
    from source.views.categories import bp as categories_bp
    from source.views.budgets import bp as budgets_bp
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(budgets_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)