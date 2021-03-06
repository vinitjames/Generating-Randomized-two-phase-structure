from src.data.database import Database


def read_config(configpath='config.txt'):
    config = {}
    config_db = Database(configpath)
    config_reader = config_db.get_reader()
    for row in config_reader:
        idx = row.index('=')
        config[row[0]] = row[idx+1:]
    config_db.close()
    return config


if __name__ == '__main__':
    print(read_config('config/CNT_config.dat'))
