#!/usr/bin/python3
import os,json,subprocess
import configparser
from flask import Flask,request,jsonify, redirect, url_for
from flask_cors import CORS, cross_origin

#Standard Flask startup code
app = Flask(__name__)
app.run(ssl_context='adhoc')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#Read configuration file in .ini format
config = configparser.ConfigParser()
config.read('threatware.ini')

#Set config variables
base = os.path.join(config['general']['rootdirectory'],'modules')
pythonpath = config['general']['pythonpath']
apiversion = config['general']['apiversion']
app.config['UPLOAD_FOLDER'] = config['general']['uploadfolder']

# API Handling Routines

#API Call:
#listModules - this call lists all available ThreatWare Modules
#Parameters: None
#
@app.route('/%s/modules/list'%apiversion)
def listModules():
	if authCheck():
		modules = []
		for module_name in os.listdir(base):
			current = os.path.join(base,module_name)
			if module_name[0] != '.' and os.path.isdir(os.path.join(base,module_name)):
				v_file = os.path.join(current,'VERSION')
				if os.path.isfile(v_file):
					v_file_h = open(v_file,"r")
					version = v_file_h.read()
					v_file_h.close()
				else:
					version = 'unknown'
			modules.append({'module':module_name,'version':version})
		return jsonify({'action':'listModules','result':modules}) 
	else:
		return jsonify({'action':'listModules','result':'Unauthorized Access','error':True})

#API Call:
#getConfig - reads the JSON config file
#Parameters: None
#
@app.route('/%s/modules/<module_name>/config'%apiversion,methods = ['GET'])
def getConfig(module_name):
	if authCheck():
		current = os.path.join(base,module_name)
		c_file = os.path.join(current,'config.json')
		if os.path.isfile(c_file):
			c_file_h = open(c_file,"r")
			config = c_file_h.read()
			c_file_h.close()
		else:
			config = ''
		return jsonify({'action':'getConfig','module':module_name,'result':config})
	else:
		return jsonify({'action':'getConfig','result':'Unauthorized Access','error':True})

#API Call:
#writeConfig - Overwites existing config file with the one passed in the form field "configuration"
#Parameters: configuration - form field
#
@app.route('/%s/modules/<module_name>/config'%apiversion,methods = ['POST'])
def writeConfig(module_name):
	if authCheck():
		current = os.path.join(base,module_name)
		c_file = os.path.join(current,'config.json')
		c_file_h = open(c_file,"w")
		data = request.json["configuration"]
		c_file_h.write(str(data))
		c_file_h.close()
		return jsonify({'action':'writeConfig','module':module_name,'result':'OK'})  
	else:
		return jsonify({'action':'writeConfig','result':'Unauthorized Access','error':True})

#API Call: 
#runModule - Executes the run.py script in the designated module directory
#Parameters: None
#
@app.route('/%s/modules/<module_name>/run'%apiversion)
def runModule(module_name):
	if authCheck():
		current = os.path.join(base,module_name)
		m_file = os.path.join(current,'run.py')
		if os.path.isfile(m_file):
			module = subprocess.run([pythonpath, 'run.py'], stdout=subprocess.PIPE, cwd=current)
			output = module.stdout
		else:
			output = ''
		return jsonify({'action':'runModule','module':module_name,'result':output.decode('UTF-8')})
	else:
		return jsonify({'action':'runModule','result':'Unauthorized Access','error':True})

#API Call:
#listResults: Provide a list of all log files in a particular module directory
#Parameters: None
#
@app.route('/%s/modules/<module_name>/results'%apiversion)
def listResults(module_name):
	if authCheck():
		results = []
		current = os.path.join(base,module_name)
		for result_file in os.listdir(current):
			if result_file[-4:] == '.log':
				results.append({'file':result_file,'date':os.stat(current).st_ctime})
		return jsonify({'action':'listResults','module':module_name,'result':results})
	else:
		return jsonify({'action':'listResults','result':'Unauthorized Access','error':True})
#API Call:
#showResults - Fetches a specified log file from the module directory
#Paramenters: logFile name (without .log) passed on the URL line
#
@app.route('/%s/modules/<module_name>/results/<id>'%apiversion)
def showResults(module_name,id):
	if authCheck():
		current = os.path.join(base,module_name,id+'.log')
		r_file_h = open(current,"r")
		output = r_file_h.read()
		r_file_h.close()
		return jsonify({'action':'showResult','module':module_name,'result':output})
	else:
		return jsonify({'action':'showResult','result':'Unauthorized Access','error':True})

#API Call:
#installModule - Allows a zipped directory containing a ThreatWare module to be uploaded
#                via a standard HTTP upload.
#Paramenters: file - containing the uploaded file.  Upload via HTTP POST.
@app.route('/%s/system/install/<filename>'%apiversion,methods=['POST'])
def installModule(filename):
	if authCheck():
		file = request.files['file']
		file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
		file.save(file_path)
		subprocess.run(['unzip',file_path ,'-d','/home/threatware/modules'])
		return jsonify({'action':'installModule','module':filename,'result':'OK'})
	else:
		return jsonify({'action':'installModule','result':'Unauthorized Access','error':True})
#Function:
#authCheck - Utility function used to check that the API is being used by an authorized application.
#
def authCheck():
	headers = request.headers
	auth = headers.get("user_token")
	if auth != config['general']['serverkey']:
		return False 
	else:	
		return True
