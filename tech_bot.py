import pandas as pd
from defs import SELL,BUY,NONE
from index_cal import IndexCalc
import joblib

class Technicals():
    def __init__(self, settings, api, pair, granularity,priceXX, log=None,  ):
        self.settings = settings
        self.api = api
        self.pair = pair
        self.log= log
        self.granularity=granularity
        self.prev_current = priceXX
        self.indexcal=IndexCalc(pair, granularity)

    def log_message(self, msg):
        if self.log is not None:
            self.log.logger.debug(msg)


    def fetch_candles(self, row_count):
        status_code, df = self.api.fetch_candles(self.pair, count=row_count, granularity=self.granularity)
        if df is None:
            self.log_message(f"erroe occured while fetching {self.pair}, time: {candle_time}, status code = {status_code}")
            return None

        # elif df.iloc[-1].time != candle_time:
        #     self.log_message(f"error fetching candle {self.pair}, time: {candle_time}, the received candles time = {df.iloc[-1].time}")
        #     return None
        else:
            return df

    def process_candles(self, df):
        df.reset_index(drop=True, inplace=True)
        df['PAIR']=self.pair
        df['SPREAD']=df.ask_c-df.bid_c

        # short_prev = 'PREV_SHORT'
        # long_prev = 'PREV_LONG'

        # short_col = f'MA_{self.settings.short_ma}'
        # long_col = f'MA_{self.settings.long_ma}'
        
        # df[short_col] = df.mid_c.rolling(window=self.settings.short_ma).mean()
        # df[long_col] = df.mid_c.rolling(window=self.settings.long_ma).mean()
        
        # df[short_prev] = df[short_col].shift(1)
        # df[long_prev] = df[long_col].shift(1)
        
        # df['D_PREV'] = df[short_prev] - df[long_prev]
        # df['D_NOW'] = df[short_col] - df[long_col]

        #magic candle settings
        df['mid_h_prev'] = df.mid_h.shift(1)
        df['mid_l_prev'] = df.mid_l.shift(1)
        df['mid_h_next'] =df.mid_h.shift(-1)
        df['mid_l_next'] =df.mid_l.shift(-1)
        df['MA_3'] =df.mid_c.rolling(window=1).mean()
        df['dy_mean']=(df.MA_3 - df.MA_3.shift(1))*10000


        df['hour'] = (pd.to_datetime(df['time'])).dt.hour 
        df['minute']=pd.to_datetime( df['time']).dt.minute

       
        spread = df.iloc[-1].ask_c -df.iloc[-1].bid_c
        dy_mean=df.iloc[-1].dy_mean
        prev_l = df.iloc[-2].mid_l
        now_l = df.iloc[-1].mid_l

        prev_h = df.iloc[-2].mid_h
        now_h = df.iloc[-1].mid_h
       

        now_o= df.iloc[-1].mid_o
        current_price_bid = df.iloc[-1].bid_c 
        current_price_ask = df.iloc[-1].ask_c  #streaming close price of the incomplete candle
        decision = None
        signal = spread*10000
        indexSignal = self.indexcal.signal()

       


        #short signal detection
        if current_price_ask - prev_l< 0:
            if dy_mean < -signal:
                if indexSignal ==-1:
                    if self.prev_current is not None:
                        if self.prev_current - prev_l<0:
                            return None, False
                    else:
                        self.prev_current= prev_l    
                        decision = -1
        #long signal detection
        elif current_price_bid - prev_h>0:
            if dy_mean > signal:
                if indexSignal == 1:
                    if self.prev_current is not None:
                        if self.prev_current - prev_h>0:
                            return None, False
                    else:
                        self.prev_current= prev_h
                        decision = 1 
        if decision == (1 ) :
            log_columns= ['time','volume','mid_o','mid_l','mid_h','mid_c','SPREAD','PAIR']
            self.log_message(f"Found a Succesfull Long or Buy trade !!!, trade open price : {current_price_bid} \n{df[log_columns].tail(3)}")
            self.log_message(f"\n Trade decison: {decision}\n")
            print("New crossing successfully detected, ready to place trade")
        if decision == ( -1) :
            log_columns= ['time','volume','mid_o','mid_l','mid_h','mid_c','SPREAD','PAIR']
            self.log_message(f"Found a Succesfull  Short or Sell trade !!!, trade open price : {current_price_ask} \n{df[log_columns].tail(3)}")
            self.log_message(f"\n Trade decison: {decision}\n")
            print("New crossing successfully detected, ready to place trade")

        if self.prev_current == None:
            print("No crossing detected")

        if decision !=None:
            rf_ml_array=[ decision,df.minute,  df.hour,df.spread,  df.ask_o, df.bid_o]
            #loading the saved model
            rf_model = joblib.load("friday_rf.joblib")
            ml_decision = int(rf_model.predict([rf_ml_array]))

            return ml_decision, self.prev_current

        return decision, self.prev_current
        






    def trade_decision(self):
        max_rows =5
        self.log_message("\n ")
        #self.log_message(f"make trade decision for pair: {self.pair} using {max_rows} candles")

        df= self.fetch_candles(max_rows)

        if df is not None:
            return self.process_candles(df)

        return None
