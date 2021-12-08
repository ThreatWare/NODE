#!/usr/bin/python3
import socket, threading, sys, os, re, json

f = open('config.json')
config = json.load(f)
f.close()

ip = config['address'] 
threads = []
open_ports = {}

table_header_html="<tr><th>Open Ports</th></tr>"
table_data_html=""

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

log_count = 1
while os.path.exists("output_%s.log"%log_count):
    log_count += 1
# The script when run using the API seems to fail at or during the next line
# This doesn't appear to be an issue when run from the Node's console   
f = open('output_%s.log'%log_count,'w')
f.write(html_output)
f.close()
print(html_output)
