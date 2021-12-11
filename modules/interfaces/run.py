#!/usr/bin/python3
import subprocess,os,re,sys
sys.path.append('../../../')
from threatware.libs.utilities import loadConfig,writeLog

#ThreatWare Module: Interfaces
#
#Decription: Reports information regarding network interfaces on the current host.
#            

#Load configuration options
config = loadConfig()

#Create the command line to be executed
command_line = config['command']+config['options']

#Execute the shell command
module = subprocess.run(command_line, stdout=subprocess.PIPE)

#Parse out the data, removing non-UTF-8 characters
command_output = module.stdout
command_output = command_output.decode('UTF-8')
command_output = command_output.split("\n")
headers = command_output[0].split()
header_html="<tr>"
for item in headers:
	header_html += "<th>%s</th>"%item
header_html += "</tr>"
interfaces = range(1,len(command_output)-1)
interface_html = ""
for interface in interfaces:
	temp_data = command_output[interface].split()
	interface_html += "<tr>"
	for item in temp_data:
		interface_html += "<td>%s</td>"%item
	interface_html += "</tr>"
html_output = "<table>%s%s</table>"%(header_html,interface_html)

#Output the results to the operator and a logfile
writeLog(html_output)
print(html_output)
