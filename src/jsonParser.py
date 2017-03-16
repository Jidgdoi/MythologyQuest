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

def readObject(jsonData, Class, Object):
	"""
	Return all objects of type Class as a dictionary.
	'jsonData': dictionary formated like JSON format.
	'Class': Class to read.
	'Object': the object of class 'Class'.
	"""
	dObject = {}
	for ID in jsonData[Class].keys():
		obj = Object()
		[setattr(obj, k, v) for k,v in jsonData[Class][ID].items()]
		dObject[ID] = obj
	return dObject

def addObject(jsonData, attr, Object):
	"""
	Add the attributes of the object 'Object' to the attribute 'attr'.
	"""
	jsonData[attr].append( vars(Object) )

def updateAttribute(jsonData, attr, (key, value)):
	"""
	
	"""
	return

def writeJson(jsonData, oFile):
	with open(oFile, "w") as fh:
		json.dump(jsonData, fh, indent=4)

# =======================
#    ===   MAIN   ===
# =======================

if __name__=='__main__':
	if len(sys.argv) == 1:
		print >> sys.stderr, "IOError: no input file.\nUsage: python2.7 update_trackList.json.py <input.json> [ <output.json> ]"
		sys.exit(0)
	else:
		iFile = sys.argv[1]
		oFile = sys.argv[2] if len(sys.argv) > 2 else None
	
	## Read JSON file
	jsonData = loadJSON(iFile)
	
	## Read Heroes
	print " HEROES ".center(25, '-')
	dh = readObject(jsonData, 'Hero', Hero)
	for i in dh.values():
		print i
	
	## Read Monsters
	print " MONSTERS ".center(25, '-')
	dm = readObject(jsonData, 'Monster', Monster)
	for i in dm.values():
		print i
	
	## Read Items
	print " ITEMS ".center(25, '-')
	di = readObject(jsonData, 'Item', Item)
	for i in di.values():
		print i
	
	# Write or print Json data
	if oFile: writeJson(jsonData, oFile)
#	else: print >> sys.stdout, json.dumps(jsonData, indent=4)

