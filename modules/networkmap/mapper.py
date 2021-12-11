#!/usr/bin/python3
import json,os,sys
import scapy.all as scapy
sys.path.append('../../../')
from threatware.libs.utilities import loadConfig, writeLog

#ThreatWare Module: Network Map
#
#Decription: Compiles a list of all machines available on the local subnet.
#

#Load configuration data
config = loadConfig()
request = scapy.ARP()

#Create an ARP request packet where the protocol destination is the network address
#and the hardware destination address is the broadcast addess
request.pdst = config['networkaddress'] 
broadcast = scapy.Ether()
broadcast.dst = 'ff:ff:ff:ff:ff:ff'
request_broadcast = broadcast / request

#Send the packet
clients = scapy.srp(request_broadcast, timeout = int(config['timeout']),verbose=False)[0]

#Compile the output as HTML
html_output = "<table><tr><th>IP Address</th><th>MAC Address</th></tr>"
for element in clients:
	html_output += "<tr><td>%s</td><td>%s</td></tr>"%(element[1].psrc,element[1].hwsrc)
html_output += "</table>"

#Write the output to the API and a log file
writeLog(html_output)
print(html_output)
