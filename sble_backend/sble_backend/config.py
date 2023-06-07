class Config(object):
    SECRET_KEY = '38a01b0a4f0faacf7f8c7839f613c9f1c5e11937f896ea746cb13f107395437c'
    USERNAME = "apikey-3730efc62a2b4511b2e06864bd07665f"
    PASSWORD = "2f597ad5576f71b62bf37603b383fa96811fc285"
    URL = "https://d4182120-61de-4f84-a811-078a6712c9d7-bluemix.cloudant.com"


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_NAME = "testing_database"


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_NAME = "production_database"


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
