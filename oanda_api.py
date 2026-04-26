import requests
import pandas as pd
import time
from dateutil.parser import *
import defs 
import utils
import sys
import json
from pprint import pprint
#from pip_calc import PipCalc

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
                 # ADD THIS — prints the actual error message from OANDA
                #print(f"HTTP {status_code} | URL: {url}")
                #print(f"Response body: {response.text}")
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
    
    # def fetch_candles(self, pair_name, count=10, granularity="H1"):
    #     url = f"{defs.OANDA_URL}/instruments/{pair_name}/candles"

    #     params = dict(
    #         granularity = granularity,
    #         price = "MBA"
    #     )
        
    #     params['count'] = count
        
    #     status_code, data = self.make_request(url, params=params)

    #     if status_code != 200:
    #         return status_code, None

    #     return status_code, OandaAPI.candles_to_df(data['candles'])





    def fetch_candles(self, pair_name, count=None, granularity="H1", date_from=None, date_to=None):
        url = f"{defs.OANDA_URL}/instruments/{pair_name}/candles"

        params = dict(
            granularity = granularity,
            price = "MBA"
        )
        
        if date_from is not None and date_to is not None:
            params['to'] = int(date_to.timestamp())
            params['from'] = int(date_from.timestamp())
        elif count is not None:
            params['count'] = count
        else:
            params['count'] = 300
        
        response = self.session.get(url, params=params, headers=defs.SECURE_HEADER)

        if response.status_code != 200:
            return response.status_code, None
        data = response.json()
        if 'candles' in data:
            df = self.candles_to_df(data['candles'])
            return response.status_code, df
        else:
            return response.status_code, None

    
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




#setting stop loss and take profit
    def trailing_sl(self, tradeID, distance ):
        url =f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/orders"
         
        data={
            "order": {
                "timeInForce": "GTC",
                "distance": str(distance),
                "type": "TRAILING_STOP_LOSS",
                "tradeID": str(tradeID),
                "triggerCondition" :"DEFAULT"
            }

        }
        status_code, json_data = self.make_request(url, verb='post', data=json.dumps(data), code_ok=201)
        ok = 201
        if status_code != ok:
            return status_code
        return True



    def fetch_instrument(self ):
        url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/instruments?instruments={self.instrument}"


        status_code, data = self.make_request(url)


        if status_code == 200:
            df = pd.DataFrame.from_dict(data['instruments'])
            self.pipLocation = float(df['pipLocation'])
            self.displayPrecision = float(df['displayPrecision'])
            return True
            #return self.pipLocation,  self.displayPrecision

            
        else:
            return None



    def pipcalc(self, distance,pair):
        
        self.distance = distance
        self.instrument=pair
        req = self.fetch_instrument()
        if req ==True:
            prec = self.displayPrecision
            dp = 10**self.pipLocation
            tsdist = self.distance * dp
            #pips= (f'{tsdist:.{prec}f}')
            return tsdist, self.pipLocation
        return False




    def placeTrade(self, pair, units, take_profit=None, stop_loss= None, trailing_stop_loss=None):
        url =f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/orders"
        #url ='https://api-fxpractice.oanda.com/v3/accounts/101-001-21389307-001/orders'
        tsl = None

        if trailing_stop_loss is not None:
            distance = trailing_stop_loss
            tsl ,pip = self.pipcalc(distance, pair)
            #return tsl, pip
            
            # "trailingStopLossOnFill":{
            #         "timeInForce":"GTC",
            #         "distance":f"{tsl}"
            #     }





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
            return None, None, None
        print(json_data)

        #getting the tradeID from the order
        tradeID = None
        sl = None
        tp = None
        #tsl= None
        
        if "orderFillTransaction" in json_data and "tradeOpened" in json_data["orderFillTransaction"]:
            tradeID = int(json_data["orderFillTransaction"]["tradeOpened"]["tradeID"])
            price = float(json_data["orderFillTransaction"]["tradeOpened"]["price"])
            
            
            if take_profit is not None:
                distance = take_profit
                tppip, x = self.pipcalc(distance, pair)
                
                if units>0:
                    tprofit = price + tppip
                elif units<0:
                    tprofit = price - tppip
                res_tp = self.set_sl_tp("TAKE_PROFIT", tprofit, tradeID)
                tp = tprofit
                if res_tp != True:
                    print('erroe occured. Take profit not set. Contact administrater, Error code= ', res_tp)
                    tp = False



            if stop_loss is not None:
                distance = stop_loss
                slpip, x = self.pipcalc(distance, pair)
                
                if units>0:
                    sloss = price - tppip
                elif units<0:
                    sloss = price + tppip
                res_sl = self.set_sl_tp("STOP_LOSS", sloss, tradeID)
                sl = sloss
                if res_sl != True:
                    print('erroe occured. Take profit not set. Contact administrater, Error code= ', res_sl)
                    sl = False
        #    if stop_loss is not None:
        #        res_sl = self.set_sl_tp("STOP_LOSS", stop_loss, tradeID)
        #        sl = stop_loss
        #        if res_sl != True:
        #            print('erroe occured. Stop loss not set. Contact administrater, Error code= ', res_sl)
        #            sl = False



            

        #    if trailing_stop_loss is not None:
        #         distance = trailing_stop_loss
        #         tsl = self.pipcalc(distance, pair)
        #         res_tsl = self.trailing_sl(tradeID, tsl)
                
        #         tsl = trailing_stop_loss
        #         if res_tsl != True:
        #             print('erroe occured. TRAILING Stop loss not set. Contact administrater, Error code= ', res_tsl)
        #             tsl = False

                
        return tradeID, sl  , tp  #, sl

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
    idx, sl, tp  =api.placeTrade("USD_CAD", 10000,stop_loss=10, take_profit=55)

    #trades =api.open_trades()
    #res = api.trailing_sl(4599, 1)
    #print(f"placed trade, id : {tradeID}")

    print(idx,sl, tp)
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
        
    