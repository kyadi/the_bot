
from oanda_api import OandaAPI
import json
import defs
import pandas as pd
from pip_calc import PipCalc

class IndexCalc():

    def __init__(self,pair,granularity):
        self.pair=pair
        self.granularity=granularity
        self.api = OandaAPI()
        self.pipcal=PipCalc(pair)
        self.piploc=self.pipcal.piploc()
        #self.tradable_pairs = []  # Ensure attribute always exists

    def fetch_candles(self,pair,  granularity, row_count=3,):
        status_code, df = self.api.fetch_candles(pair, count=row_count, granularity=granularity)
        if df is None:
            return None
        else:
            return df

    def get_pairs_from_string(self, pair_str):
        #existing_pairs = cls.get_instruments_dict().keys()
        pairs = pair_str.split(",")
        
        pair_list = []
        for p1 in pairs:
            for p2 in pairs:
                p = f"{p1}_{p2}"
                #if p in existing_pairs:
                pair_list.append(p)
        
        return pair_list

    

    
    
    def v_per(self,pair):
        df = self.fetch_candles(pair, self.granularity)
        if df is None:
            print('df is none')
            return None, None

        #print(df)

        prev_o = df.iloc[-2].mid_o
        prev_c = df.iloc[-2].mid_c
        prev_perc =  ((prev_c/prev_o) -1)*100




        open_price=df.iloc[-1].mid_o
        close_price=df.iloc[-1].mid_c
        
        
        
        perc = ((close_price/open_price) -1)*100
       
        return perc, prev_perc
        

 
    
    def fetch_instruments(self):
        url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/instruments"
        status_code, data = self.api.make_request(url)
        tradable_pairs = []
        adf=[]
        if status_code == 200:
            df = (data['instruments'])
            for x in df:

                
                tradable_pairs.append(x['name'])
                
            #adff=pd.DataFrame.to_dict(adf)
            # for x in adf:
            #     tradable_pairs.append(str(x))
            self.tradable_pairs=tradable_pairs
            return self.tradable_pairs
        else:
            return None
        
        

    def resultate_index(self,instrument):
        self.fetch_instruments()
        pairs_str = "GBP,EUR,USD,CAD,JPY,NZD,CHF,SGD,AUD"
        pair_list = self.get_pairs_from_string(pairs_str)
        pairs=[]
        existing_pairs=self.tradable_pairs

        for pair in pair_list:
            if pair.startswith(instrument) == True:
                pairs.append(pair)
            if pair.endswith(instrument) == True:
                pairs.append(pair)

        #print(pairs)

        r = 0
        prev_r=0
        for p in pairs:
            if p in existing_pairs:
                #print(p)

                perc, prev_perc = self.v_per(p)
                if p.startswith(instrument) == True:
                    r = r + perc
                    prev_r =prev_r + prev_perc
                   # print(p)
                elif p.endswith(instrument) == True:
                    r = r - perc
                    prev_r =prev_r - prev_perc
                    #print(p)

        resultant_percetage = r
        #print(resultant_percetage,prev_r )

        return  resultant_percetage



    def signal(self):
        pair =self.pair
        a1 = pair[0:3]
        a2= pair[-3:] 
        a1_index = self.resultate_index(a1)
        a2_index = self.resultate_index(a2)

        if a1_index>0 and a2_index<0:
            return 1
        elif a1_index<0 and a2_index>0:
            return -1
        return 0


    def stopTrade(self):
        granularity='M5'
        df = self.fetch_candles(self.pair,granularity, row_count=5)
        if df is not None:

            v1 = df.iloc[-5].mid_c - df.iloc[-5].mid_o
            v2 = df.iloc[-4].mid_c - df.iloc[-4].mid_o
            v3 = df.iloc[-3].mid_c - df.iloc[-3].mid_o
            v4 = df.iloc[-2].mid_c - df.iloc[-2].mid_o

            last_close=df.iloc[-2].mid_c
            pip= -self.piploc
            total_volume = v1+v2+v3+v4
            total_pips= (total_volume)*10**pip


            if total_pips>8:
                return 1
            elif total_pips<-8:
                return-1
            else:
                return 0
            print(total_pips)
            print(last_close)
            
            print(self.piploc)
        return None




if __name__=='__main__':
    a=IndexCalc('EUR_GBP','H1' )
    #ans =a.v_per('USD_GBP')
    #a.resultate_index('NZD')
    #ans=a.fetch_instruments()
    ans =a.stopTrade()
    print(ans)


