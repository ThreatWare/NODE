#!/usr/bin/python3
import socket, threading, sys, os, re
sys.path.append('../../../')
from threatware.libs.utilities import loadConfig, writeLog

#ThreatWare Module: Port Scan
#
#Decription: uses python threads to scan a machine for open ports.
#

#Load configuration data
config = loadConfig()
ip = config['address'] 
threads = []
open_ports = {}

table_header_html="<tr><th>Open Ports</th></tr>"
table_data_html=""

#try_port: Creates a socket and attempts to connect.
#Returns True if the socket is open, otherwise it returns False
def try_port(ip, port, open_ports):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(5)
    result = sock.connect_ex((ip, port))

    if result == 0:
        open_ports[port] = 'open'
        return True
    else:
        open_ports[port] = 'closed'
        return None

#scan_port: itterates through all port numbers, spawns a thread for each attempt
#then waits for them to complete and compiles the results
def scan_ports(ip):
    
    table_data=""
    
    for port in range(0, 65535):
        thread = threading.Thread(target=try_port, args=(ip, port, open_ports))
        threads.append(thread)

    for i in range(0, 65535):
        threads[i].start()

    for i in range(0, 65535):
        threads[i].join()

    for i in range (0, 65535):
        if open_ports[i] == 'open':
            table_data += "<tr><td>%s</td></tr>"%str(i)
            
    return table_data

try:
    table_data_html = scan_ports(ip)
    
except KeyboardInterrupt:
    sys.exit()

except socket.gaierror:
    sys.exit()

except socket.error:
    sys.exit()

html_output = "<table>%s%s</table>"%(table_header_html,table_data_html)

#Return the results to the API caller and write it to a log file
writeLog(html_output)
print(html_output)
