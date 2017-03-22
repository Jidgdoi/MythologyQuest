#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

import Utility.Colors as Colors
from Cell import Cell
from collections import deque

class World():
	"""
	Object representing the entire flat world.
	"""
	def __init__(self, *args):
		## Load list of maps
		self.dMap = {}
		self.cellMap = []
		for filename in args:
			self.loadMap(filename)

	def __repr__(self):
		## Colors associated to each features.
		dColor = {}
		for s in ("water", "forest", "path"):
			bg = "blue" if s == "water" else "green" if s == "forest" else ""
			for i in ("hero", "treasure", "trap", ""):
				t = "H" if i == "hero" else "T" if i == "treasure" else "^" if i == "trap" else " "
				dColor[(s,i)] = Colors.color(fgColor="red",bgColor=bg)(t)
		
		txt = ''
		for line in self.cellMap:
			previousCellType = False
			for cell in line:
				if previousCellType:
					# Space between 2 walls: set features wall for the space
					if cell.surface == "path": txt += dColor[(cell.surface,cell.item)]
					elif previousCellType == "path": txt += dColor[(cell.surface,cell.item)]
					elif previousCellType == cell.surface: txt += dColor[(cell.surface,cell.item)]
					elif previousCellType != cell.surface: txt += dColor[(cell.surface,cell.item)]
					# Just a space
					else: txt += ' '
				txt += dColor[(cell.surface,cell.item)]
				previousCellType = dColor[(cell.surface,cell.item)]
			txt += '\n'
		return txt

	def loadMap(self, filename):
		"""
		Load a map and store it in a dictionary as {'Map name': lMap}.
		'filename': filename of the map.
		"""
		lMap = deque()
		fh = open(filename, 'r')
		mapname = fh.readline().strip()
		if self.dMap.has_key(mapname):
			print >> sys.stderr, "[ \033[1;31mWarning\033[0m ] The map '%s' has already been loaded."
		line = fh.readline()
		while line:
			lMap.append( deque(line.strip().split(';')) )
			line = fh.readline()
		fh.close()
		self.dMap[mapname] = lMap

	def cellulizeMap(self, mapname):
		"""
		Cellulize a map, which means create the map with Cell objects.
		"""
		dCellMap = deque()
		for x in xrange(len(self.dMap[mapname])):
			dCellMap.append( deque() )
			for y in xrange(len(self.dMap[mapname][x])):
				surface, (hero,treasure,trap) = self.decodeMapCell(self.dMap[mapname][x][y])
				dCellMap[x].append( Cell(surface, hero, treasure, trap) )
		self.cellMap = dCellMap

	def decodeMapCell(self, code):
		"""
		Decode a cell of a map.
		"""
		args = [False, False, False]
		for i in code:
			if i in 'wfp': surface = {'w':"water", 'f':"forest", 'p':"path"}[i]
			elif i == 'h': args[0] = "hero"
			elif i == 't': args[1] = "treasure"
			elif i == 'T': args[2] = "trap"
		return surface, args
