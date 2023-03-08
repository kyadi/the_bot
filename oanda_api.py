import requests
import pandas as pd
import time
from dateutil.parser import *
import defs
import utils
import sys
import json
from pprint import pprint

from oanda_trade import Oanda_trade


class OandaAPI():

    def __init__(self):
        self.session = requests.Session()    

    def make_request(self, url, params={}, added_headers=None, verb='get', data=None, code_ok=200):

        headers = defs.SECURE_HEADER

        if added_headers is not None:   
            for k in added_headers.keys():
                headers[k] = added_headers[k]
                
        try:
            response = None
            if verb == 'post':
                response = self.session.post(url,params=params,headers=headers,data=data)
            elif verb == 'put':
                response = self.session.put(url,params=params,headers=headers,data=data)
            else:
                response = self.session.get(url,params=params,headers=headers,data=data)

            status_code = response.status_code

            if status_code == code_ok:
                json_response = response.json()
                return status_code, json_response
            else:
                return status_code, None   

        except:
            print("ERROR")
            
            return 400, None   

    def fetch_instruments(self):
        url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/instruments"
        status_code, data = self.make_request(url)
        return status_code, data
    
    def get_instruments_df(self):
        status_code, data = self.fetch_instruments()
        if status_code == 200:
            df = pd.DataFrame.from_dict(data['instruments'])
            return df[['name', 'type', 'displayName', 'pipLocation', 'marginRate']]
        else:
            return None
    
    def fetch_candles(self, pair_name, count=10, granularity="H1"):
        url = f"{defs.OANDA_URL}/instruments/{pair_name}/candles"

        params = dict(
            granularity = granularity,
            price = "MBA"
        )
        
        params['count'] = count
        
        status_code, data = self.make_request(url, params=params)

        if status_code != 200:
            return status_code, None

        return status_code, OandaAPI.candles_to_df(data['candles'])

    
    def last_complete_candle_time(self, pair_name, granularity="H1"):
        code, df = self.fetch_candles(pair_name, granularity=granularity)
        if df is None:
            print("erroe occured while fetching candles. Error code : ", code )
            return None
        return df.iloc[-2].time

    

    def incomplete_candle(self, pair_name, granularity="H1"):
        code, df = self.fetch_candles(pair_name, granularity=granularity)
        if df is None:
            print("error occured while fetching candles. Error code : ", code )
            return None
        return df.iloc[-1]

    def current_price(self,  pair_name, granularity="H1"):
        df1 = (api.incomplete_candle(pair_name, granularity=granularity))
        price = df1.mid_c
        return price


    def last_complete_candle(self, pair_name, granularity="H1"):
        code, df = self.fetch_candles(pair_name, granularity=granularity)
        if df is None:
            print("erroe occured while fetching candles. Error code : ", code )
            return None
        return df.iloc[-2].time


    def close_trade(self, trade_id):
        url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/trades/{trade_id}/close"
        status_code, json_data = self.make_request(url, verb='put', code_ok=200)

        if status_code == 200:
            print("You have succefully closed the trade with Id= ", trade_id)
            return True, status_code           
        elif status_code == 400:
            print("failed to closed the trade with Id= ", trade_id)
            return False, status_code
        elif status_code == 404:
            print("There doesnot exist a trade with Id= ", trade_id)
            return False, status_code
        else:
            print("Unkown error occured, contact administrator")




#setting stop loss and take profit
    def set_sl_tp(self, order_type, price, tradeID):
        url =f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/orders"
        
        data={
            "order": {
                "timeInForce": "GTC",
                "price": str(price),
                "type": str(order_type),
                "tradeID": str(tradeID)
            }

        }
        status_code, json_data = self.make_request(url, verb='post', data=json.dumps(data), code_ok=201)
        ok = 201
        if status_code != ok:
            return status_code
        return True




    def placeTrade(self, pair, units, take_profit=None, stop_loss= None):
        #url =f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/orders"
        url ='https://api-fxpractice.oanda.com/v3/accounts/101-001-21389307-001/orders'

        data={
            "order": {
                "units": units,
                "instrument": pair,
                "timeInForce": "FOK",
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }

        }
        status_code, json_data = self.make_request(url, verb='post', data=json.dumps(data), code_ok=201)
        ok = 201
        if status_code != ok:
            print("An error occured while placing the trade. Error code: ", status_code)
            return None
        #print(json_data)

        #getting the tradeID from the order
        tradeID = None
        sl = None
        tp = None
        
        if "orderFillTransaction" in json_data and "tradeOpened" in json_data["orderFillTransaction"]:
           tradeID = int(json_data["orderFillTransaction"]["tradeOpened"]["tradeID"])
           if take_profit is not None:
               res_tp = self.set_sl_tp("TAKE_PROFIT", take_profit, tradeID)
               tp = take_profit
               if res_tp != True:
                   print('erroe occured. Take profit not set. Contact administrater, Error code= ', res_tp)
                   tp = False
           if stop_loss is not None:
               res_sl = self.set_sl_tp("STOP_LOSS", stop_loss, tradeID)
               sl = stop_loss
               if res_sl != True:
                   print('erroe occured. Stop loss not set. Contact administrater, Error code= ', res_tp)
                   sl = False
                
        return tradeID, tp, sl

    def open_trades(self):
        url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/openTrades"
        status_code, data = self.make_request(url)
        if status_code != 200:
            print(f"An error occured. Error code : {status_code}")
            
            return None
        
        trades = [Oanda_trade.Trade_from_api(x) for x in data['trades']]

        return trades



    @classmethod
    def candles_to_df(cls, json_data):
        prices = ['mid', 'bid', 'ask']
        ohlc = ['o', 'h', 'l', 'c']

        our_data = []
        for candle in json_data:

            #commented out in order to get the current imcomplete candle so as we get the live data as if streaming api 
            ''' if candle['complete'] == False:
                continue '''
            new_dict = {}
            new_dict['time'] = candle['time']
            new_dict['volume'] = candle['volume']
            for price in prices:
                for oh in ohlc:
                    new_dict[f"{price}_{oh}"] = float(candle[price][oh])
            our_data.append(new_dict)
        df = pd.DataFrame.from_dict(our_data)
        df["time"] = [parse(x) for x in df.time]
        return df


if __name__ == "__main__":
    api = OandaAPI()
    #res, df = api.fetch_candles("EUR_USD", granularity="M5")
    #tradeID, tp, sl =api.placeTrade("EUR_USD", 200)

    trades =api.open_trades()
    #print(f"placed trade, id : {tradeID}")

    print(trades)
    # print(api.last_complete_candle("EUR_USD", granularity="M5"))
    # while True:
    #     df1 = (api.incomplete_candle("EUR_USD", granularity="H4"))s
    #     df2 = (api.incomplete_candle("EUR_USD", granularity="S5"))
    #     #current_price = api.current_price("AUD_JPY", granularity="H4")
    #     price = df1.mid_c
    #     price2=df2.mid_c
    #     timee =df2.time
    #     SLEEP = 3
    
        
    #     print(price, timee, price2)
    #     time.sleep(3)
        
    