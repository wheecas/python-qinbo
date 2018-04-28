import configparser

cf = configparser.ConfigParser()
cf.read("config.ini")

def getConfigValue(name):
    value = cf.get("config", name)
    return value

def testHour():
    return getConfigValue(name="hour")
