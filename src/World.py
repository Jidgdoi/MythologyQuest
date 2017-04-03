#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

from Cell import Cell
from collections import deque

from src.Utility.Utils import SCREEN_DIM

class World():
	"""
	Object representing the entire flat world.
	"""
	def __init__(self, filename):
		self.mapName = "default"
		## Attributes storing map
		self.rawMap = []
		self.cellMap = []
		## Map dimension
		self.width = 0
		self.height = 0
		## Hero position
		self.hero_x = 0
		self.hero_y = 0
		## Treasure and trap coordinates
		self.lCoordTreasure = []
		self.lCoordTrap = []
		
		## Load and create map
		self.loadMap(filename)
		self.cellulizeMap()

	def loadMap(self, filename):
		"""
		Load a map.
		Update attributes: mapName, txtMap, hero_x, hero_y, lCoordTreasure, lCoordTrap, width and height
		'filename': filename of the map.
		"""
		self.rawMap = deque()
		fh = open(filename, 'r')
		# First line: Map name
		self.mapName = fh.readline().strip()
		# Second line: Hero position
		self.hero_x, self.hero_y = map(int, fh.readline().strip().split(';'))
		# Third line: Treasures coordinates
		self.lCoordTreasure = [map(int, i.split(';')) for i in fh.readline().strip().split(' ')]
		# Fourth line: Traps coordinates
		self.lCoordTrap = [map(int, i.split(';')) for i in fh.readline().strip().split(' ')]
		
		# Next lines: the map
		line = fh.readline()
		while line:
			self.rawMap.append( deque(line.strip().split(';')) )
			line = fh.readline()
		fh.close()
		
		# Set attributes
		self.width = len(self.rawMap[0])
		self.height = len(self.rawMap)

	def cellulizeMap(self):
		"""
		Cellulize a map, which means create the map with Cell objects.
		Update attribute cellMap
		"""
		self.cellMap = deque()
		for i in xrange(self.height):
			self.cellMap.append( deque() )
			for j in xrange(self.width):
				surface = self.decodeMapCell(self.rawMap[i][j])
				hero     = True if (i,j) == (self.hero_x, self.hero_y) else False
				treasure = True if (i,j) in self.lCoordTreasure else False
				trap     = True if (i,j) in self.lCoordTrap else False
				self.cellMap[i].append( Cell(surface, j, i, self.hero_x, self.hero_y, hero, treasure, trap) )

	def decodeMapCell(self, code):
		"""Decode a map's cell."""
		return {'w':"water", 'f':"forest", 'p':"path", 'n':"none", 'W':"wall"}[code]

	def getCellSprites(self, hero_x=None, hero_y=None):
		"""
		Return all the cell.sprite attributes.
		"""
		if not hero_x: hero_x = self.hero_x
		if not hero_y: hero_y = self.hero_y
		lSprite = []
		for i in xrange(hero_y - SCREEN_DIM[1]/2 -1, hero_y + SCREEN_DIM[1]/2 +1):
			for j in xrange(hero_x - SCREEN_DIM[0]/2 -1, hero_x + SCREEN_DIM[0]/2 +1):
				if i < 0 or i >= self.height: continue
				if j < 0 or j >= self.width: continue
				lSprite.append( self.cellMap[i][j].sprite )
		return lSprite
