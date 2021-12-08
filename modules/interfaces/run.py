#!/usr/bin/python3
import json,subprocess,os,re
f = open('config.json')
config = json.load(f)
f.close()
command_line = config['command']+config['options']
module = subprocess.run(command_line, stdout=subprocess.PIPE)
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
log_files = []
file_pattern = re.compile('output_(\d?).log')
for file_name in os.listdir('.'):
	matches = file_pattern.match(file_name)
	if matches:
		log_files.append(matches.group(1))
log_files.sort(reverse=True)
f = open('output_%d.log'%(int(log_files[0])+1),'w')
f.write(html_output) 
f.close()
print(html_output)
