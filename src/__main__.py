#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

import os,sys
from Hero import Hero
from Monster import Monster
from Item import Item
from World import World
import jsonParser
import threading,Queue

if __name__=='__main__':
	## Load JSON file
	jsonData = jsonParser.loadJSON('../data/default.json')
	
	## Read Heroes
	print " HEROES ".center(25, '-')
	dh = jsonParser.readObject(jsonData, 'Hero', Hero)
	for i in dh.values():
		print i
	
	## Read Monsters
	print " MONSTERS ".center(25, '-')
	dm = jsonParser.readObject(jsonData, 'Monster', Monster)
	for i in dm.values():
		print i
	
	## Read Items
	print " ITEMS ".center(25, '-')
	di = jsonParser.readObject(jsonData, 'Item', Item)
	for i in di.values():
		print i
