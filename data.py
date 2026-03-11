import csv
with open('data.csv','r') as f:
    data=csv.reader(f)
    lis=[]
    for row in data:
        lis.append(row)
sno=[]
c_ticks=[]
c_time=[]
p_ticks=[]
p_time=[]
for row in lis:
    sno.append(row[0])
    c_ticks.append(row[1])
    c_time.append(row[2])
    p_ticks.append(row[3])
    p_time.append(row[4])
print("Number of Data",sno[1:])
print("Cimple Tick Count",c_ticks[1:])
print("Cimple Runtime",c_time[1:])
print("Python Tick Count",p_ticks[1:])
print("Python Runtime",p_time[1:])