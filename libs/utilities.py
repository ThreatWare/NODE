#!/usr/bin/python3
import json, os
def loadConfig():
	f = open('config.json')
	config = json.load(f)
	f.close()
	return config
def writeLog(html_output):
	log_count = 1
	log_filename = "output_%s.log"%log_count
	while os.path.exists(log_filename):
		log_count += 1
		log_filename = "output_%s.log"%log_count
	f = open(log_filename,'w')
	f.write(html_output)
	f.close()

