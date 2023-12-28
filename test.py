import configparser


def writeConfigSection(section: str):
    parser = configparser.ConfigParser()
    parser.read("config.data")
    print(dict(parser[section].items()))


if __name__ == '__main__':
    writeConfigSection("General")
