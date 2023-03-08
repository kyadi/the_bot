from dateutil.parser import parse
class Oanda_trade():
    def __init__(self, oanda_obj):
        self.instrument = (oanda_obj['instrument'])
        self.trade_id = int(oanda_obj['id'])
        
        #self.financing= float(oanda_obj['financing'])
        
        #self.initialUnits = (oanda_obj['initialUnits'])
        
        #self.openTime = parse(oanda_obj['openTime'])
        self.price = float(oanda_obj['price'])
        #self.realizedPL = float(oanda_obj['realizedPL'])
        self.Units = int(oanda_obj['currentUnits'])
        #self.state = (oanda_obj['state'])
        self.Profits = float(oanda_obj['unrealizedPL'])

    def __repr__(self):
        return str(vars(self))
        
    @classmethod
    def Trade_from_api(cls, api_object):
        return Oanda_trade(api_object)