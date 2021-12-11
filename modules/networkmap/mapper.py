#!/usr/bin/python3
import json,os,sys
import scapy.all as scapy
sys.path.append('../../../')
from threatware.libs.utilities import loadConfig, writeLog
config = loadConfig()
request = scapy.ARP()

request.pdst = config['networkaddress'] 
broadcast = scapy.Ether()

broadcast.dst = 'ff:ff:ff:ff:ff:ff'

request_broadcast = broadcast / request
clients = scapy.srp(request_broadcast, timeout = int(config['timeout']),verbose=False)[0]
html_output = "<table><tr><th>IP Address</th><th>MAC Address</th></tr>"
for element in clients:
	html_output += "<tr><td>%s</td><td>%s</td></tr>"%(element[1].psrc,element[1].hwsrc)
html_output += "</table>"
writeLog(html_output)
print(html_output)
