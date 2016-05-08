#!/usr/bin/env python
import numpy as np
import sys
import os



def parent():
	# =======================================================
	# Read data from Standard Input
	# =======================================================

	# Read from Standard Input into data variable
	data = sys.stdin.readlines()

	employeeList = []
	hours = {}

	lineCounter = 0

	for line in data:
	    tokens = line.split()
	    if(not tokens):
	       continue
	 
	    lineCounter = lineCounter + 1
	    
	#   Parse the first line (employee list)
	    if(lineCounter == 1):
	       employeeList = tokens

	#   Parse the rest lines (date list)
	    if(tokens and lineCounter > 1):
	      if(tokens[0] not in hours):
		 hours[tokens[0]] = {}
	      dict_copy = hours[tokens[0]].copy()
	      dict_copy.update({tokens[1]:tokens[2:]})
	      hours[tokens[0]] = dict_copy
	

	# FORK()
	new_PID = os.fork()
        if new_PID == 0:
            child(employeeList, hours)
        else:
            print "\nHello from PARENT:  \nPARENT ID: ", os.getpid(), ", CHILD ID: ", new_PID


def child(employeeList, hours):
	# =======================================================
	# Output to Standard Output
	# =======================================================

	# Message from CHILD
	print 'Hello from CHILD:  \nCHILD ID: ', os.getpid()

	sys.stdout.write("===============================================================================\n")
	sys.stdout.write("\nOUTPUT RESULT\n")
	sys.stdout.write("===============================================================================\n")

	presence_hours = 0
	employee_Presence_Hours = {}

	unexpected_workers_byDate = {}

	datesList = sorted(list(hours.keys()))
	for date in datesList:
	#   Output to standard output : DATE
	    sys.stdout.write(date + " ")
	#   Output to standard output : HOURS
	    hoursList = sorted(list(hours[date].keys()))
	    for hour in hoursList:
	       sys.stdout.write(hour + " ")
	    sys.stdout.write("\n")

	#   Output to standard output : EMPLOYEE list and their presence
	    for empl in employeeList:
	       sys.stdout.write(empl + "     ")
	       for hour in hoursList:
		  if(empl in hours[date][hour]):
		     sys.stdout.write('Y     ')
		     presence_hours = presence_hours + 1
		  else:
		     sys.stdout.write('N     ')
	       sys.stdout.write("\n")
	#      Count each EMPLOYEEs presence hours
	       employee_Presence_Hours[empl] = presence_hours
	       presence_hours = 0
	    sys.stdout.write("\n")
	#   Output to standard output : each EMPLOYEEs presence hours
	    sys.stdout.write(date + " ")
	    for empl in employeeList:
	       sys.stdout.write(empl + ":" + str(employee_Presence_Hours[empl]) + " ")
	    sys.stdout.write("\n")

	#   Output to standard output : unexpected workers
	    unexpected_workers_byHour = {}
	    for hour in hoursList:
	       unexpected_workers_byHour[hour] = [e for e in hours[date][hour] if e not in employeeList]
	       if(unexpected_workers_byHour[hour]):
		  sys.stdout.write("Unexpected worker ID on " + date + " at " + hour + " [ " + ", ".join(unexpected_workers_byHour[hour]) + " ]\n")
	    unexpected_workers_byDate[date] = unexpected_workers_byHour
	    sys.stdout.write("\n")

if __name__ == "__main__":
	parent()
	
