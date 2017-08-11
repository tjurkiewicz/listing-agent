import config


def test_config():
    conf = config.get_config('test_data/config.ini')

    assert conf['SQLDatabase']['Connection'] == 'driver://db:db@localhost/db'
    assert conf['Queue']['Host'] == 'localhost'
    assert conf['Queue']['Username'] == 'username'
    assert conf['Queue']['Password'] == 'password'
    assert conf['Queue']['Exchange'] == 'exchange'
    assert conf.getint('Runtime', 'Interval') == 60
