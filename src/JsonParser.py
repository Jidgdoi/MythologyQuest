# -*- coding:utf-8 -*-

# Cyril Fournier
# 10/08/2016

# =======================================
# Update the trackList.json of a JBrowse,
# by adding category, description, color
# =======================================

import os,sys
import json
from Hero import Hero
from Monster import Monster
from Item import Item

# ============================
#    ===   FUNCTIONS   ===
# ============================

def loadJSON(filename):
	"""
	Load a JSON file.
	Output is a nested dictionary: {'Class': {'ID': {'attribute': value}}}.
	'filename': JSON file to load.
	"""
	return json.loads( open(filename,"r").read() )

def readObject(jsonData, Class):
	"""
	Return all objects of type Class as a dictionary.
	'jsonData': dictionary formated to JSON format.
	'Class': Class to read.
	"""
	dObject = {}
	for ID in jsonData[Class.__name__].keys():
		obj = Class()
		[setattr(obj, k, v) for k,v in jsonData[Class.__name__][ID].items()]
		dObject[ID] = obj
	return dObject

def addObject(jsonData, Object):
	"""
	Add the instance of 'Object' to the JSON.
	'jsonData': dictionary formated to JSON format.
	'Object': Object to add.
	"""
	if jsonData[Object.__class__.__name__].has_key( Object.id ): print >> sys.stderr, "Error: the Object ID '%s' already exist in the JSON Data." %Object.id
	else: jsonData[Object.__class__.__name__][Object.id] = vars(Object)

def writeJson(jsonData, oFile):
	with open(oFile, "w") as fh:
		json.dump(jsonData, fh, indent=4)

def printJson(jsonData):
	print >> sys.stdout, json.dumps(jsonData, indent=4)

# =======================
#    ===   TEST   ===
# =======================

if __name__=='__main__':
	if len(sys.argv) == 1:
		print >> sys.stderr, "IOError: no input file.\nUsage: python2.7 update_trackList.json.py <input.json> [ <output.json> ]"
		sys.exit(0)
	else:
		iFile = sys.argv[1]
		oFile = sys.argv[2] if len(sys.argv) > 2 else None
	
	## Load JSON file
	jsonData = loadJSON(iFile)
	
	## Read JSON data and create objects.
	dObj = {}
	for Class in [Hero, Monster, Item]:
		print " {} ".format(Class.__name__.upper()).center(25, '-')
		dTmp = readObject(jsonData, Class)
		dObj.update( dTmp )
		for i in dTmp.values():
			print i
	
	addObject(jsonData, dObj['h1'])
	addObject(jsonData, Hero(name='Rufus'))
	
	# Write or print Json data
	if oFile: writeJson(jsonData, oFile)
	else: printJson(jsonData)

