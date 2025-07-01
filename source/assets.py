from flask_assets import Environment, Bundle

def init_assets(app):
    assets_env = Environment(app)
    assets_env.load_path = ['styles']
    scss_bundle = Bundle(
        'main.scss',
        filters='libsass',
        output='css/main.css',
        depends='**/*scss'
    )
    assets_env.register('scss_all', scss_bundle)
    # Em modo debug, compila na hora
    scss_bundle.build()