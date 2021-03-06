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

def loadJSONmap(filehandler):
	"""
	Load the JSON part of a map file.
	'filehandler": file object
	"""
	return json.loads( filehandler.read() )

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
		if Class.__name__ == 'Hero': obj.activeSprite()
		dObject[ID] = obj
	return dObject

def addObject(jsonData, Object):
	"""
	Add the instance of 'Object' to the JSON.
	'jsonData': dictionary formated to JSON format.
	'Object': Object to add.
	"""
	if jsonData[Object.__class__.__name__].has_key( Object.id ): print("Error: the Object ID '%s' already exist in the JSON Data." %Object.id, file=sys.stderr)
	else: jsonData[Object.__class__.__name__][Object.id] = vars(Object)

def writeJson(jsonData, oFile):
	with open(oFile, "w") as fh:
		json.dump(jsonData, fh, indent=4)

def printJson(jsonData):
	print(json.dumps(jsonData, indent=4), file=sys.stderr)
