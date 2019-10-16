import io
import os
import sys
from flask import Flask
from flask.logging import default_handler
from functools import wraps, partial
import logging

from .utils import ContextualFilter, log_file_handler
from .utils import req_id_log_formatter

CONFIG_NAME_MAPPER = {
    "local": "local_config.LocalConfig",
    "development": "config.DevelopmentConfig",
    "testing": "config.TestingConfig",
    "stage": "config.StageConfig",
    "production": "config.ProductionConfig",
}


def create_app(app_name=__name__, flask_config_name=None, **kwargs):

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    app = Flask(app_name, **kwargs)

    app.logger.addFilter(ContextualFilter())  # pylint: disable=no-member
    default_handler.setFormatter(req_id_log_formatter())

    env_flask_config_name = os.getenv("FLASK_CONFIG")
    if not env_flask_config_name and flask_config_name is None:
        flask_config_name = "local"
    elif flask_config_name is None:
        flask_config_name = env_flask_config_name
    else:
        if env_flask_config_name:
            assert env_flask_config_name == flask_config_name, (
                'FLASK_CONFIG environment variable ("%s") and flask_config_name argument '
                '("%s") are both set and are not the same.'
                % (env_flask_config_name, flask_config_name)
            )

    try:
        app.config.from_object(CONFIG_NAME_MAPPER[flask_config_name])
        app.logger.setLevel(  # pylint: disable=no-member
            app.config.get("LOG_LEVEL", logging.ERROR)
        )
        if app.config.get("ENABLE_LOG_FILE", False):
            log_file_dir = app.config.get("LOG_FILE_DIR", "log")
            app.logger.addHandler(  # pylint: disable=no-member
                log_file_handler(log_file_dir, "app.log")
            )
    except ImportError:
        if flask_config_name == "local":
            app.logger.error(  # pylint: disable=no-member
                "You have to have `local_config.py` or `local_config/__init__.py` in order to use "
                "the default 'local' Flask Config. Alternatively, you may set `FLASK_CONFIG` "
                "environment variable to one of the following options: development, stage, production, "
                "testing."
            )
            sys.exit(1)
        raise

    return app


def register_init(api, app=None):
    """Register init_app function to api

    Arguments:
        api {flask_restplus.Namespace} -- api namespace
    """

    def outer_wrapper(f):
        @wraps(f)
        def wrapper():
            if app:
                if not app.config.get("SWAGGER_DOC", False):
                    api._doc = False
                app.init = partial(f, api=api, app=app)
            else:
                bond_f = partial(f, api)
                api.init = bond_f

        wrapper()

    return outer_wrapper


def register_apis(api, namespace_list, app):
    def inner(app):
        if not app.config.get("SWAGGER_DOC", False):
            api._doc = False
        api.init_app(app)

        for ns in namespace_list:
            ns.init(app)  # pylint: disable=no-member

    app.init = partial(inner, app)
