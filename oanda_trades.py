

from oanda_api import OandaAPI
import defs
import utils
import pprint

import pandas as pd
pd.set_option('display.max_columns', None)


import calendar
import datetime as dt

from dateutil.parser import *




class OandaTrades():
    
    def __init__(self,pair,granularity):

        self.pair=pair
        self.granularity=granularity
        self.api = OandaAPI()


    def fetch_records(self):
        url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/positions/EUR_USD"
        status_code, data = self.api.make_request(url)
        return status_code, data

    def fetch_transaction(self,start_date,end_date):
        url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/transactions?to={end_date}&from={start_date}"
        status_code, data = self.api.make_request(url)
        if status_code == 200:
            return data
        else:
            print(f'error occured during fetch date transactions...',+ status_code)
            return False

    def fetch_id_range(self, link):
        url = link
        status_code, data = self.api.make_request(url)
        if status_code == 200:
            return data
        else:
            print(f'error occured during  id range fetching...',+ status_code)
            return False

    
    
    def applyProfits(self,row):
            
        d=row.tradesClosed[0]
        dprof=d['realizedPL']
        return dprof

    def applyid(self,row):
            
        d=row.tradesClosed[0]
        Id=d['tradeID']
        return Id

    def applyUnits(self,row):
        d=row.tradeOpened
        units=int(d['units'])
        if units>0:
            return  1
        elif units<0:
            return -1
        return None

    def applyAsk(self,row):
        d = row['fullPrice']
        ask=d['closeoutAsk']
        return  ask

    def applyBid(self,row):
        d = row['fullPrice']
        bid=d['closeoutBid']
        return  bid


    def applyClosetime(self,row):
        d = row['time']
        ts = parse(d)

        time =ts.time()
        return  time

    def applyOpentime(self,row):
        d = row['time']
        ts = parse(d)

        time =ts.time()
        return  time

    


    def applyDay(self,row):
        d = row['time']
        ts = parse(d)
        date=ts.weekday()
        #WEEKDAYS = [ 'Tue', 'Wed', 'Thur', 'FrI', 'Sat','Sun','Mon']
        day= calendar.day_name[date]   
        return  day

    def applyDate(self,row):
        d = row['time']
        ts = parse(d)
        date=ts.date()

            
        return  date

    def apply2id(self,row):
        d=row.tradeOpened
        Id=d['tradeID']
        return Id


    


    def filterData(self,raw_data):
        df = pd.DataFrame.from_dict(raw_data['transactions'])
        df1=df[['id', 'time', 'instrument', 'reason', 'tradesClosed','fullPrice']]
        df1.dropna(subset=['tradesClosed'],inplace=True)
        #d=df1['tradesClosed']
        df['tradesClosed'] = df['tradesClosed'].astype(object)
        df1['realizedPL']=df1.apply(self.applyProfits, axis=1)
        #df1['decission']=df1.apply(self.applyUnits, axis=1)
        df1['askCloseT']=df1.apply(self.applyAsk, axis=1)
        df1['bidClose']=df1.apply(self.applyBid, axis=1)
        df1['closeTime']=df1.apply(self.applyClosetime, axis=1)
        df1['tradeId']=df1.apply(self.applyid, axis=1)


        df1['day']=df1.apply(self.applyDay, axis=1)
        df1['date']=df1.apply(self.applyDate, axis=1)
       

        df2=df[['id', 'time', 'reason', 'tradeOpened','fullPrice']]
        df2.dropna(subset=['tradeOpened'],inplace=True)
        df2['tradeId']=df2.apply(self.apply2id, axis=1)
        
        df2['openTime']=df2.apply(self.applyOpentime, axis=1)
        df2['askOpen']=df2.apply(self.applyAsk, axis=1)
        df2['bidOpenT']=df2.apply(self.applyBid, axis=1)
        df2['decission']=df2.apply(self.applyUnits, axis=1)
        

        df1sort = df1.sort_values(by="tradeId",ascending=True ) 
        df2sort = df2.sort_values(by="tradeId",ascending=True )     
        #df12merge = df1sort.join(df2sort)

        df12m=df1sort.merge(df2sort[['tradeId', 'openTime','askOpen','bidOpenT','decission']], left_on='tradeId', right_on='tradeId')

        final_df=df12m[['tradeId','date', 'day','openTime','closeTime', 'instrument', 'realizedPL', 'decission','askOpen','bidOpenT','askCloseT','bidClose']]


        #print(df2sort)
        #print(df12m)
        
        return final_df



       # final_df=df[['name', 'type', 'displayName', 'pipLocation', 'marginRate']]


    def process_data(self,data):
        pageLinks=data['pages']

        dfx =pd.DataFrame(columns=['tradeId','date', 'day','openTime','closeTime', 'instrument', 'realizedPL', 'decission','askOpen','bidOpenT','askCloseT','bidClose'])
       # pprint.pprint(pageLinks)
        for link in pageLinks:
            raw_data= self.fetch_id_range(link)
            df= self.filterData(raw_data)
            #dfx.append(df, ignore_index=True)
            dfx= pd.concat([dfx, df],ignore_index=True)
            #break
            

        print(dfx)
        dfx.to_csv('trades.csv', index=False)
            
            


        


    def run(self):

        
        s="2022-06-01T19%3A00%3A00Z"
        e="2022-07-07T00%3A00%3A00Z"

        #start =parse(s)
        #end =parse(e)

        data =self.fetch_transaction(s,e)
        self.process_data(data)
        
        #print("working", s, e)
        #print(data)
        #pass



if __name__ == "__main__":
    results = OandaTrades("EUR/JPY",'H1')
    results.run()



    #code, data =results.fetch_records()
        
    #print("")
        
