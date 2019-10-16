from config import DevelopmentConfig


class LocalConfig(DevelopmentConfig):
    ENABLE_LOG_FILE = True
    pass
