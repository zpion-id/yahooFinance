import yahooFinance as yf
import os

if __name__ == "__main__" :
    print("Program dimulai...")
    s = yf.yFinance()

    s.get_all_time("TLKM")
    print(s.status("TLKM"))

    #for sym in listStock.list :
    #    s.get_all_time(sym)
    #    print(s.status(sym))
    
    
    #s.get_range("TLKM","2005-1-31","2019-10-30")

    print("Program selesai.")