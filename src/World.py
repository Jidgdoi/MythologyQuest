#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

import pygame

from Cell import Cell
from collections import deque
import src.JsonParser as JsonParser

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
		self.sprites = pygame.sprite.Group()
		## Map dimension
		self.width = 0
		self.height = 0
		## Hero position
		self.hero_cell_x = 0
		self.hero_cell_y = 0
		self.hero_pixel_x = 0
		self.hero_pixel_y = 0
		## Treasure and trap coordinates
		self.lCoordTreasure = []
		self.lCoordTrap = []
		
		## Load and create map
		self.loadMap(filename)
		self.cellulizeMap()
		
		# Hero movement
		self.change_x = 0
		self.change_y = 0

	def changePos(self, x, y):
		self.change_pixel_x += x
		self.change_pixel_y += y

	def convertPixelToCell(self, x, y):
		"""Return a tuple with cell positions."""
		return (x / SCREEN_DIM[0], y / SCREEN_DIM[1])

	def convertCellToPixel(self, x, y):
		"""Return a tuple with pixel positions."""
		return (x * SCREEN_DIM[0], y * SCREEN_DIM[1])

	def loadMap(self, filename):
		"""
		Load a map.
		Update attributes: mapName, txtMap, hero_x, hero_y, lCoordTreasure, lCoordTrap, width and height
		'filename': map filename.
		"""
		## Read map part of file
		self.rawMap = deque()
		fh = open(filename, 'r')
		line = fh.readline()
		while line != '\n':
			self.rawMap.append( deque(line.strip().split(';')) )
			line = fh.readline()
		
		## Read JSON content's part of file
		content = JsonParser.loadJSONmap(fh)
		
		fh.close()
		
		# Set attributes
		self.width = len(self.rawMap[0])
		self.height = len(self.rawMap)
		
		for k,v in content['Map'].items():
			if hasattr(self, k): setattr(self, k, v)
			else: print "\033[1;31mError\033[0m: the attribute '{}' doesn\'t exist.".format(k)
		
		self.hero_pixel_x, self.hero_pixel_y = self.convertCellToPixel(self.hero_cell_x, self.hero_cell_y)

	def cellulizeMap(self):
		"""
		Cellulize a map, which means create the map with Cell objects.
		Update attribute cellMap.
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

	def update(self):
		self.hero_pixel_x += self.change_pixel_x
		self.hero_pixel_y += self.change_pixel_y
		
		for pos, sprite in self.dSprite.items():
			x,y = self.convertPixelToCell(self.hero_pixel_x - (SCREEN_DIM[0]/2), self.hero_pixel_y - (SCREEN_DIM[1]/2))
			cell_x += pos[0]
			cell_y += pos[1]
			
#			if sprite:
#				if sprite.
			
		
		lSprite = []
		for i in xrange(self.hero_y - SCREEN_DIM[1]/2 -1, self.hero_y + SCREEN_DIM[1]/2 +1):
			for j in xrange(self.hero_x - SCREEN_DIM[0]/2 -1, self.hero_x + SCREEN_DIM[0]/2 +1):
				if i < 0 or i >= self.height: continue
				if j < 0 or j >= self.width: continue
				lSprite.append( self.cellMap[i][j].sprite )
		return lSprite
		
