from flask import Flask
from config import Config
from pathlib import Path

import os


def create_app(testing=False):
    """ Application factory

    Args:
        testing (bool): Will load TestingConfig if True, defaults fo False
    Returns:
        The Flask application object
    """

    app = Flask(__name__)
    # TODO config
    # Dynamically load config based on the testing argument or FLASK_ENV environment variable
    flask_env = os.getenv("FLASK_ENV", None)
    if testing:
        app.config.from_object(Config)
    elif flask_env == "development":
        app.config.from_object(Config)
    elif flask_env == "testing":
        app.config.from_object(Config)
    else:
        app.config.from_object(Config)

    from app.front_end import frontEnd
    app.register_blueprint(frontEnd)

    wdir = os.path.abspath(__file__)
    p = Path(wdir).parent
    os.chdir(p)
    print(os.getcwd())

    return app
