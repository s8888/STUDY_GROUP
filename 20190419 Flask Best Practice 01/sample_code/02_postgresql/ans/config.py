DB_URI = 'postgresql://{user}:{pw}@{host}:{port}/{db}'


class Config(object):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    POSTGRES = {
        'user': 'admin',
        'pw': '1234',
        'db': 'test_db',
        'host': 'test_db-postgres',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = DB_URI.format(**POSTGRES)


class StageConfig(Config):
    POSTGRES = {
        'user': 'admin',
        'pw': '1234',
        'db': 'stage_db',
        'host': 'stage_db-postgres',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = DB_URI.format(**POSTGRES)


config = {
    'development': DevelopmentConfig,
    'stage': StageConfig
}
