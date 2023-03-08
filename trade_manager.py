from settings import Settings
from oanda_api import OandaAPI
import json
class TradeManager():

    def __init__(self, api, settings, log=None):
    #def __init__(self, api,  log=None):
        self.api=api
        self.settings = settings
        self.log = log
        self.settings = Settings.loadSettings()

    def log_message(self, msg):
        if self.log is not None:
            self.log.logger.debug(msg)

    
    
    def close_trades(self, pairs_to_close):
        open_trades = self.api.open_trades()
        if open_trades is None:
            print('error occured, open trade list not fetched')
            self.log.logger.debug('error occured, open trade list not fetched')
            msg = "Returned none while trying tho get  open trades "
            return msg
            
        pairs= pairs_to_close
        open_pairs = [trade.instrument for trade in open_trades ]
        
        trade_ids_to_close = [trade.trade_id for trade in open_trades if trade.instrument in pairs]
        #open_trade_ids=[trade.trade_id for trade in open_trades ]
        
        self.log_message(f"TradeManager:place_trade()  pairs_to_close:{pairs_to_close}")
        self.log_message(f"TradeManager:place_trade()  open trade:{open_trades}")
        self.log_message(f"TradeManager:place_trade()  trade ids to close{trade_ids_to_close}")

        for id in trade_ids_to_close:
            ok, code = self.api.close_trade(id)
            if ok == False:
                self.log_message(f"TradeManager:place_trade()  Failed to close trade with id :{id}. Error code : {code}")
                msg = "failed to close an open trade with id :{id}. Error code : {code}"
                return msg
            else:
                self.log_message(f"TradeManager:place_trade()  Successfuly closed trade with id :{id}.Status code : {code}")
                return True


    def create_trades(self, pairs_to_trade):
        self.log_message(f"TradeManager:place_trade(){pairs_to_trade}")
        for t in pairs_to_trade:
            
            pair= t['pair']
            units = t['units']
            #return t
            
            trade_id, TP, SL = self.api.placeTrade(pair, units)
            if trade_id is not None:
                self.log_message(f"TradeManager:place_trade()   Opened trade {t['pair']} with id : {trade_id}")
                
                print(f" you have successfuly placed the trade, instrument: {pair}, units: {units}. trade id is: {trade_id} ")
                return True
            else:
                msg = f"failed to open trade  {t} instrument"
                return msg

    
    
    def place_trade(self, pairs_to_trade):
        self.log_message(f"TradeManager:place_trade(){pairs_to_trade}")
        print('working')
        pairs = [x['pair'] for x in pairs_to_trade]
        self.close_trades(pairs)
        x=self.create_trades(pairs_to_trade)


        #x = pairs_to_trade
        #return x
        # 
        
        # 

if __name__ == "__main__":
    api = OandaAPI()
    #yu=[{"pair": "GBP_USD", "units": 1000, "short_ma":8, "long_ma": 32}]
    trades_to_open =[{'pair': "EUR_JPY", 'units': 100 }]
    ghj= TradeManager(api)
    ans = ghj.place_trade(trades_to_open)
    print(ans)


        