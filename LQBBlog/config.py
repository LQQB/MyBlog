class Config(object):
    """Base config class."""
    SECRET_KEY = 'LQQB'
    pass

class ProdConfig(Config):
    """Production config class."""
    pass

class DevConfig(Config):
    """Development config class."""
    # Open the DEBUG
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/myblog?charset=utf8'

    CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:15672//"
    CELERY_BROKER_URL = "amqp://guest:guest@localhost:15672//"

    #### Flask-Cache's config
    CACHE_TYPE = 'simple'   # 缓存配置

    ASSETS_DEBUG = True

    BABEL_DEFAULT_LOCALE = 'zh_CN'