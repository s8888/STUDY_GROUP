import os
import logging
import yaml


class BaseConfig(object):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    CONFIG_ROOT = os.path.join(PROJECT_ROOT, "configs")

    # Swagger UI
    SWAGGER_DOC = True

    # disable swagger X-Fields
    RESTPLUS_MASK_SWAGGER = False

    # logging setting, default: False
    LOG_LEVEL = logging.DEBUG
    if os.getenv("ENABLE_LOG_FILE") == "True":
        ENABLE_LOG_FILE = True
    else:
        ENABLE_LOG_FILE = False
    LOG_FILE_DIR = os.path.join(PROJECT_ROOT, "log")

    # back file setting, default: False
    if os.getenv("ENABLE_BACK_FILE") == "True":
        ENABLE_BACK_FILE = True
    else:
        ENABLE_BACK_FILE = False
    BACK_FILE_DIR = os.path.join(PROJECT_ROOT, "back_file")

    # for python app.py
    HOST = "0.0.0.0"
    PORT = 6001


class ProductionConfig(BaseConfig):
    # FLASK_CONFIG = production
    with open(os.path.join(BaseConfig.CONFIG_ROOT, "prod_config.yaml")) as f:
        APP_CONFIG = yaml.safe_load(f)

    LOG_LEVEL = logging.INFO
    SWAGGER_DOC = False


class StageConfig(BaseConfig):
    # FLASK_CONFIG = stage
    with open(os.path.join(BaseConfig.CONFIG_ROOT, "stage_config.yaml")) as f:
        APP_CONFIG = yaml.safe_load(f)


class DevelopmentConfig(BaseConfig):
    # FLASK_CONFIG = development
    # DEBUG = True
    with open(os.path.join(BaseConfig.CONFIG_ROOT, "dev_config.yaml")) as f:
        APP_CONFIG = yaml.safe_load(f)


class TestingConfig(BaseConfig):
    # TODO: for unit test
    TESTING = True
