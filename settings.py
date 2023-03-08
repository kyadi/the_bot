import json

class Settings():
    def __init__(self, pair, units, short_ma, long_ma):
        self.pair = pair
        self.units = units
        self.short_ma = short_ma
        self.long_ma = long_ma

    #printing out the variables of the object
    def __repr__(self):
        return str(vars(self))

    @classmethod
    def object_from_list(cls, object):
        return Settings(object['pair'], object['units'], object['short_ma'],object['long_ma'])


    #loading the settings using a class method
    @classmethod
    def loadSettings(cls):
        data = json.loads(open('settings.json', 'r').read())
        return {k:cls.object_from_list(x) for k,x in data.items()}


    @classmethod
    def get_pairs(cls):
        #settings = cls.loadSettings()
        return list(cls.loadSettings().keys())


if __name__ =="__main__":
    [print(k,x) for k,x in Settings.loadSettings().items()]
    print(Settings.get_pairs())