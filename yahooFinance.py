import requests
import re
import os
import json
import time
import datetime

import listStock

class yFinance :

    symbol = ""
    startDate = "2000-1-1"
    endDate = ""
    pathCsv = ""
    dateFormat = "%Y-%m-%d"
    market = ""

    def __init__(self,pathData="csv", market="JK"):
        self.endDate = datetime.datetime.now().strftime(self.dateFormat)

        self.market = market
        
        if not os.path.exists(pathData):
            os.mkdir(pathData)
            self.pathCsv = pathData
        else :
            self.pathCsv = pathData

    def __epochTime (self,date):
        return int(time.mktime(time.strptime(str(date),self.dateFormat)))
    
    def __regex(self, html):
        return re.search(r'"CrumbStore":\{"crumb":("[^"]+")\}', html)

    def __req (self):
        symbol = self.symbol
        start = self.__epochTime(self.startDate)
        end = self.__epochTime(self.endDate)

        session = requests.session()
        res = session.get(
            f'https://finance.yahoo.com/quote/{symbol}/history?period1={start}&period2={end}&interval=1d&filter=history&frequency=1d')
        
        res.raise_for_status()
        
        get_crumb = self.__regex(res.content.decode('utf-8'))
        
        assert get_crumb
        
        crumb = json.loads(get_crumb.group(1))
        
        get_csv = session.get(
            f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={start}&period2={end}&interval=1d&events=history&crumb={crumb}')
        
        get_csv.raise_for_status()
        return get_csv.content
    
    def __fileWrite (self,file):
        with open('{}/{}.csv'.format(self.pathCsv,self.symbol), "w") as filecsv:
            filecsv.writelines(str(file))
        
    def __valid_date (self,date):
        try:
            datetime.datetime.strptime(date, self.dateFormat)
        except ValueError:
            raise ValueError("Format tanggal salah, seharusnya YYYY-MM-DD")
    
    def status (self, symbol):

        filePath = "{}/{}.{}.csv".format(self.pathCsv,symbol,self.market)
        if os.path.isfile(filePath):
            size = os.path.getsize(filePath)
            return "{} file size {} sudah didownload.".format(symbol,"%.2f %s" % (size/1024.0, "KB"))

    def get_all_time(self, symbol):
        self.symbol = "{}.{}".format(symbol,self.market)
        csv = self.__req()
        csv = csv.decode('utf-8')
        self.__fileWrite(csv)

    def get_range(self, symbol, startDate, endDate):
        
        self.symbol = "{}.{}".format(symbol,self.market)
        self.__valid_date(startDate)
        self.__valid_date(endDate)
        self.startDate = startDate
        self.endDate = endDate
        csv = self.__req()
        csv = csv.decode('utf-8')
        self.__fileWrite(csv)
