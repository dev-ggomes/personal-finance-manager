from flask import Flask
from source.db import engine
from source.models import Base

# Inicializa o app Flask
def create_app():
    app = Flask(__name__, template_folder='templates')

    # Garante que o DB existe
    Base.metadata.create_all(engine)

    # Regista blueprints
    from source.views.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)