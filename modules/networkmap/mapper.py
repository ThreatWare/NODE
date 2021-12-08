#!/usr/bin/python3
import json,os,re
import scapy.all as scapy
f = open('config.json')
config = json.load(f)
f.close()
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
log_count = 1
log_filename = "output_%s.log"%log_count
while os.path.exists(log_filename):
        log_count += 1
        log_filename = "output_%s.log"%log_count
f = open(log_filename,'w')
f.write(html_output) 
f.close()
print(html_output)
