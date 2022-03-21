import configparser

class config:

    def write(self, section, option, value):
        cp = configparser.ConfigParser()
        cp.read('config.ini')
        cp.set(section, option, value)
        try:
            with open('config.ini', 'w') as configfile:
                cp.write(configfile)
        except:
            return False
        else:
            return True
    
    def read(self, section, option):
        cp = configparser.ConfigParser()
        cp.read('config.ini')
        value = cp.get(section, option)
        return value