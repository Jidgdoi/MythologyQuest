#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

import os,sys
from Hero import Hero
from Monster import Monster
from Item import Item
from Cell import Cell
from World import World
import JsonParser
import threading,Queue


def getRootDir():
	return os.sep.join(os.path.realpath(sys.argv[0]).split(os.sep)[:-2])

if __name__=='__main__':
	rootDir = getRootDir()
	
	## Load JSON file
	defaultDataFile = os.sep.join([rootDir, "data", "default.json"])
	jsonData = JsonParser.loadJSON( defaultDataFile )
	
	## Read Heroes
	print " HEROES ".center(25, '-')
	dh = JsonParser.readObject(jsonData, 'Hero', Hero)
	for i in dh.values():
		print i
	
	## Read Monsters
	print " MONSTERS ".center(25, '-')
	dm = JsonParser.readObject(jsonData, 'Monster', Monster)
	for i in dm.values():
		print i
	
	## Read Items
	print " ITEMS ".center(25, '-')
	di = JsonParser.readObject(jsonData, 'Item', Item)
	for i in di.values():
		print i
	
	## Create Cells
	lCells = []
	lCells.append( [Cell(0,i, "water") for i in xrange(10)] )
	lCells.append( [Cell(1,i, "water") for i in xrange(10)] )
	lCells.append( [Cell(2,i, "forest") for i in xrange(10)] )
	lCells.append( [Cell(3,i, "forest") for i in xrange(10)] )
	lCells.append( [Cell(4,i, "forest") for i in xrange(10)] )
	
	[lCells[1][i].update(surface="forest") for i in [3,4,5]]
	[lCells[i][4].update(surface="path") for i in [2,3,4]]
	lCells[3][4].update(hero=True)
	
	txt = ''
	for line in lCells:
		previousCellType = False
		for cell in line:
			if previousCellType:
				# Space between 2 walls: set features wall for the space
				if cell.surface == "path": txt += cell.design
				elif previousCellType == "path": txt += cell.design
				elif previousCellType == cell.surface: txt += cell.design
				elif previousCellType != cell.surface: txt += cell.design
				# Just a space
				else: txt += ' '
			txt += cell.design
			previousCellType = cell.surface
		txt += '\n'
	print txt





