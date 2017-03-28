#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

import os,sys
import time
import JsonParser
import random as rd

from Hero import Hero
from Monster import Monster
from Item import Item
from Spell import Spell
from Cell import Cell
from World import World
import Graphic
import Utility.Colors as Colors

def getRootDir():
	return os.sep.join(os.path.realpath(sys.argv[0]).split(os.sep)[:-2])

if __name__=='__main__':
	rootDir = getRootDir()
	
	## ======================================
	## Initiate threads and the wx app
	## ======================================
	
	## ======================================
	## Load JSON file
	## ======================================
	defaultDataFile = os.sep.join([rootDir, "data", "default.json"])
	jsonData = JsonParser.loadJSON( defaultDataFile )
	
	
	## Read JSON data and create objects.
	dObj = {}
	for Class in [Hero, Monster, Item, Spell]:
		print " {} ".format(Class.__name__.upper()).center(25, '-')
		dTmp = JsonParser.readObject(jsonData, Class)
		dObj.update( dTmp )
		for i in dTmp.values():
			print i
	print
	
	print rd.randint(dObj["s1"].action["add"]["health"][0], dObj["s1"].action["add"]["health"][1])
	
	## Load map
	mapDir = os.sep.join([rootDir, "data", "map"])
	world = World()
	world.loadMap("%s%sdefault.txt"%(mapDir, os.sep))
	
	cellMap = world.cellulizeMap("Default map")
	
	print Graphic.terminalOutput( world.cellMap )
