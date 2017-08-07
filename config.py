import configparser


def get_config(path='/etc/listing-parser/config.ini'):
    config = configparser.ConfigParser()
    config.read(path)

    return config