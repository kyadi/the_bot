  
from oanda_api import OandaAPI
import defs 
import math
import pandas as pd


class PipCalc():
    def __init__(self,pair):
        self.distance = None
        self.instrument = pair
        self.api = OandaAPI()
        self.pipLocation = None
        self.displayPrecision = None





    def make_request(self, url, params={}, added_headers=None, verb='get', data=None, code_ok=200):
    
        headers = defs.SECURE_HEADER

        if added_headers is not None:   
            for k in added_headers.keys():
                headers[k] = added_headers[k]
                
        try:
            response = None
            status_code = None
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
            
            return status_code, None  
    



    def fetch_instrument(self ):
        url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/instruments?instruments={self.instrument}"


        status_code, data = self.api.make_request(url)


        if status_code == 200:
            df = pd.DataFrame.from_dict(data['instruments'])
            self.pipLocation = float(df['pipLocation'].iloc[0])
            self.displayPrecision = float(df['displayPrecision'].iloc[0])
            return True
            #return self.pipLocation,  self.displayPrecision

            
        else:
            return status_code



    def calc(self, distance,pair):
        
        self.distance = distance
        self.instrument=pair
        req = self.fetch_instrument()
        if req ==True:
            prec = self.displayPrecision
            dp = 10**self.pipLocation
            tsdist = self.distance * dp
            #pips= (f'{tsdist:.{prec}f}')
            return tsdist
        return False

    def piploc(self):
        self.fetch_instrument()
        return self.pipLocation


if __name__ == "__main__":
    tc = PipCalc()
    #print(tc.fetch_instrument())
    print(tc.calc(25, 'GBP_USD'))








