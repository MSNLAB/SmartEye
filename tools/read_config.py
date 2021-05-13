import configparser
import os


def read_config(section, key=None):

    root_path = os.path.abspath(os.path.dirname(__file__))
    config = configparser.ConfigParser()
    config.read(root_path + "/../config/config.ini")
    if key is None:
        items = config.items(section)
        models = []
        for item in items:
            models.append(item[1])
        return models
    else:
        value = config.get(section, key)
        return value

if __name__ == '__main__':
    result = read_config("classes-file")
    print(result)
