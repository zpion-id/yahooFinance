import requests
import re
import os
import json
import time
import datetime

import listStock

class YFinance :

    symbol = ""
    __startDate = "2000-1-1"
    __endDate = ""
    pathCsv = ""
    dateFormat = "%Y-%m-%d"
    market = ""

    def __init__(self,pathData="csv", marketID="JK"):
        self.__endDate = datetime.datetime.now().strftime(self.dateFormat)

        self.market = marketID
        
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
        start = self.__epochTime(self.__startDate)
        end = self.__epochTime(self.__endDate)

        session = requests.session()
        res = session.get(
            f'https://finance.yahoo.com/quote/{symbol}/history?period1={start}&period2={end}&interval=1d&filter=history&frequency=1d')
        
        res.raise_for_status()
        
        get_crumb = self.__regex(res.content.decode('utf-8'))
        
        assert get_crumb , exit("data tidak ditemukan")
        
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
            return "{}.{}.csv file size {} sudah didownload.".format(symbol,self.market,"%.2f %s" % (size/1024.0, "KB"))

    def get_all_time(self, symbol):
        self.symbol = "{}.{}".format(symbol,self.market)
        csv = self.__req()
        csv = csv.decode('utf-8')
        self.__fileWrite(csv)

    def get_range(self, symbol, start_date, end_date):
        
        self.symbol = "{}.{}".format(symbol,self.market)
        self.__valid_date(start_date)
        self.__valid_date(end_date)
        self.__startDate = start_date
        self.__endDate = end_date
        csv = self.__req()
        csv = csv.decode('utf-8')
        self.__fileWrite(csv)
