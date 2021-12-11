#!/usr/bin/python3
import os
from datetime import date

#ThreatWare Module: Network Map 
#
#Decription: Compiles a list of all machines available on the local subnet.
#

#This script requires root access.  Use sudo to grant it.
os.execvp("sudo",["sudo","/usr/bin/python3","mapper.py"])
