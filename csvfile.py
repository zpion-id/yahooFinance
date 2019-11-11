import csv

def csv_to_list (filecsv = '',) :
    with open(filecsv, newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        listcsv = []
        for row in spamreader:
            listcsv.append(row)
        return listcsv

def show_csv (filecsv = '',) :
    with open(filecsv, newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        data = ''
        for row in spamreader:
            data += ', '.join(row)+"\n"
        
        print (data)

show_csv('csv/JSMR.JK.csv')
#print(csv_to_list('csv/JSMR.JK.csv')[2])