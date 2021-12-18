!/usr/bin/python3
# Use below for macos python 3.10
#Library/Frameworks/Python.framework/Versions/3.10/bin/python3
# Note: install python3 as: apt-get install python3 or yum install python3 or see https://python.org
# Note: you must install pythonping module as: pip3 install pythonping
import os
from datetime import datetime
from pythonping import ping

def get_hostname(a):
    result = str(os.popen('nslookup ' +a).read())
    parts = result.split("=")
    mylen = len(parts)
    return(parts[mylen-1].strip()+",")

#subnet = "10.1.10.0"
subnet = "192.168.1.0"

def date_time():
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")
    return(str(date_time+","))

datenow = date_time()
datenow = datenow.replace(" ","-")
datenow = datenow.replace("/","-")
datenow = datenow.replace(":","")

report_name = "/tmp/ping_report_for_subnet_"+subnet+"_"+datenow[:-1]+".csv"
myfd = open(report_name,"w")

print ("Program running. performing pings on subnet: "+subnet)
print ("progress will be printed below. WAIT for the word FINISHED....")
print (" ")
print("date            IP            hostname  payload size  ping time in ms")
print("____            __            ________  ____________  _______________")
parts = subnet.split(".")

subnet = parts[0] + "." + parts[1] + "." + parts[2] + "."
myfd.write("date,IP,hostname,payload size,ping time in ms\n")
for mynum in range(1, 255):
    ipaddr = subnet + str(mynum)
    result = str(ping(ipaddr, count=1))
    lines = result.split("\n")
    if "Reply from " in lines[0]:
        parts = lines[0].split(" ")
        #print (lines[0])
        print(date_time()+parts[2][:-1]+","+get_hostname(parts[2][:-1])+parts[3]+" "+parts[4]+","+parts[6])
        myfd.write(date_time()+parts[2][:-1]+","+get_hostname(parts[2][:-1])+parts[3]+" "+parts[4]+","+parts[6]+"\n")
myfd.flush()
myfd.close()
print ("Finished.")
print (" ")
print ("cat "+report_name)
print ("mv "+report_name+" ~")
