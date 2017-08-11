import configparser
import logging.config


def get_config(path='/etc/listing-parser/config.ini'):
    config = configparser.ConfigParser()
    config.read(path)

    return config


def setup():
    logging.config.dictConfig(DEFAULT_LOGGING)


DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s:%(levelname)s:%(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    }
}