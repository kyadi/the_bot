import pprint
import time
from settings import Settings
from log_wrapper import LogWrapper

from oanda_api import OandaAPI
from timing import Timing
from technicals import Technicals
from defs import SELL, BUY, NONE
from trade_manager import TradeManager
#from index_cal import IndexCalc
GRANULARITY ="H1"
SLEEP = 3.0


class TradingBot():

    def __init__(self, pair):
        self.log = LogWrapper("TradingBot")
        self.tech_log = LogWrapper("TechnicalsBot")
        self.trade_log = LogWrapper("TradeLogs")
        self.api = OandaAPI()
        
        self.trade_pairs =  [pair]
        self.settings = Settings.loadSettings()
        self.timings ={p: Timing(self.api.last_complete_candle_time(p, GRANULARITY)) for p in self.trade_pairs }
        self.log_message(f"Bot started with the following settings :\n { pprint.pformat(self.settings) } ")
        self.log_message(f"Bot timings :\n { pprint.pformat(self.timings) } ")
        self.trade_manager = TradeManager(self.api, self.settings, self.trade_log)
        self.priceX=None
        self.switch = False
        #self.indexcal=IndexCalc(pair, GRANULARITY)
        self.decision=0
        #self.decision = None


    def log_message(self, msg):
        self.log.logger.debug(msg)

    def new_candle(self):
        for pair in self.trade_pairs:
            complete_candle_time = self.api.last_complete_candle_time(pair, GRANULARITY)
            # self.timings[pair].ready= False
            if complete_candle_time> self.timings[pair].last_complete_candle:
                self.timings[pair].last_complete_candle = complete_candle_time
                self.log_message(f"{pair}, new candle {complete_candle_time}")
                return True
            #     self.timings[pair].ready= True
            #     
    def close_trade(self):
        pair = self.trade_pairs
        ans = self.trade_manager.close_trades(pair)
        if ans is True:
            print(f"Closed the {self.trade_pairs} was closed because a new candle was received")
        # else:
        #     print(f"New candle received but trade {self.trade_pairs} was not closed. error : {code}")


    def process_pairs(self, priceX):
        trades_to_open =[]
        #units = 1000
        for pair in self.trade_pairs:
            #if self.timings[pair].ready == True:
            self.log_message(f"checking for a trade on: {pair}")
            pricexx = priceX
            techs = Technicals(self.settings[pair], self.api, pair, GRANULARITY, pricexx, log=self.tech_log )
            decision, Xprice = techs.trade_decision()
            self.priceX = Xprice
            
            
            if decision is not None:
                units = self.settings[pair].units * decision
                trades_to_open.append({'pair': pair, 'units': units })
                self.decision=decision

        if len(trades_to_open) > 0:
            print(trades_to_open)
            for m in trades_to_open:
                d=self.trade_manager.place_trade(m)

                #print(d)
                print(d, decision, self.priceX, "\n  \n  \n")
            


    #the loop
    def run(self):
        while True:
            print('processing ....')
            #print('updating timings .....')
            is_new_candle = self.new_candle()
            print('processing pairs .....')
            #if new candle received, set self.price to none
            if is_new_candle == True:
                self.priceX = None
                #close the open trade
                print("New candle received, Closing any open trade in progress")
                self.close_trade()
                
                
            else:
                print("no new candle received")    
            self.process_pairs(self.priceX)
            '''if self.priceX is not None:
                stoptrade = self.indexcal.stopTrade()
                if self.decision>0:
                    if stoptrade<0:
                        self.close_trade()
                if self.decision<0:
                    if stoptrade>0:
                        self.close_trade()'''





            print('refreshing .....')
            time.sleep(SLEEP)

if __name__ == "__main__":
    b = TradingBot("NZD_CAD")
    d = TradingBot("EUR_JPY")
    e = TradingBot("EUR_USD")
    #b.run()
    #d.run()
    e.run()
    