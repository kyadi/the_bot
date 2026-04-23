from settings import Settings
from oanda_api import OandaAPI
import json

from pip_calc import PipCalc
class TradeManager():

    def __init__(self, api, settings=None, log=None):
        self.api = api
        self.settings = settings or Settings.loadSettings()
        self.log = log
        self.trailingStoploss = 6
        self.takeProfit = 5
        self.stoploss = 5
        # Per-pair state: multiplier and last outcome
        import os
        self.state_file = 'pair_state.json'
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    self.pair_state = json.load(f)
            except Exception:
                self.pair_state = {pair: {'multiplier': 1, 'last_outcome': None} for pair in self.settings.keys()}
        else:
            self.pair_state = {pair: {'multiplier': 1, 'last_outcome': None} for pair in self.settings.keys()}

    def save_pair_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.pair_state, f)

    def update_lot_multiplier(self, pair, outcome):
        if outcome == 'TP_HIT':
            self.pair_state[pair]['multiplier'] = 1
        elif outcome in ['LOSS', 'SL_HIT', 'NO_TP']:
            self.pair_state[pair]['multiplier'] *= 2
        self.pair_state[pair]['last_outcome'] = outcome
        self.save_pair_state()

    def get_lot_multiplier(self, pair):
        return self.pair_state.get(pair, {}).get('multiplier', 1)

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
                msg = f"failed to close an open trade with id :{id}. Error code : {code}"
                return msg
            else:
                self.log_message(f"TradeManager:place_trade()  Successfuly closed trade with id :{id}.Status code : {code}")
                return True


    def create_trades(self, pairs_to_trade):
        self.log_message(f"TradeManager:place_trade(){pairs_to_trade}")
        t = pairs_to_trade
        pair = t['pair']
        base_units = self.settings[pair].units
        multiplier = self.get_lot_multiplier(pair)
        units = base_units * multiplier * (1 if t['units'] > 0 else -1)
        trade_id, dis, tp = self.api.placeTrade(pair, units, stop_loss=self.stoploss, trailing_stop_loss=self.trailingStoploss, take_profit=self.takeProfit)
        if trade_id is not None:
            self.log_message(f"TradeManager:place_trade()   Opened trade {t['pair']} with id : {trade_id}")
            print(f" you have successfuly placed the trade, instrument: {pair}, units: {units}. trade id is: {trade_id} ")
            # Simulate outcome detection (replace with real logic)
            # For now, assume TP hit if tp is not None, else loss
            if tp:
                self.update_lot_multiplier(pair, 'TP_HIT')
            else:
                self.update_lot_multiplier(pair, 'LOSS')
            return True
        else:
            msg = f"failed to open trade  {t} instrument"
            return msg
        
        # for t in pairs_to_trade:
            
        #     pair= t['pair']
        #     units = t['units']
        #     #return t
            
        #     trade_id, TP, SL = self.api.placeTrade(pair, units)
        #     if trade_id is not None:
        #         self.log_message(f"TradeManager:place_trade()   Opened trade {t['pair']} with id : {trade_id}")
                
        #         print(f" you have successfuly placed the trade, instrument: {pair}, units: {units}. trade id is: {trade_id} ")
        #         return True
        #     else:
        #         msg = f"failed to open trade  {t} instrument"
        #         return msg

    
    
    def place_trade(self, pairs_to_trade):
        self.log_message(f"TradeManager:place_trade(){pairs_to_trade}")
        print('working')
        x = pairs_to_trade
        #pairs = [x['pair'] for x in pairs_to_trade]
        pair = x['pair'] 
        self.close_trades(pair)
        self.create_trades(pairs_to_trade)


        #x = pairs_to_trade
        return pair
        # 
        
        # 

if __name__ == "__main__":
    api = OandaAPI()
    #setig = Settings(pair, units, short_ma, long_ma)
    #yu=[{"pair": "GBP_USD", "units": 1000, "short_ma":8, "long_ma": 32}]
    trades_to_open =[{'pair': "EUR_JPY", 'units': 100 }]
    ghj= TradeManager(api)
    ans = ghj.place_trade(trades_to_open)
    print(ans)


        