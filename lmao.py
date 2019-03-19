import pandas as pd
import csv

months = []
with open('2017.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            months = row[1::]
            break


d2017=pd.read_csv('2017.csv')
d2018=pd.read_csv('2018.csv')


#FINDING MAX AND MIN
avg = []
for row in months:
    p=d2017[row].min()
    q=d2018[row].min()
    avg.append((p+q)/2)


print(avg)
