#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

import pygame
import numpy as np

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

	def get_hero_pos(self):
		return np.array([self.hero_cell_x, self.hero_cell_y])

	def convertPixelToCell(self, (x, y)):
		""" Return a tuple with cell positions."""
		return np.array((x / SCREEN_DIM[0], y / SCREEN_DIM[1]))

	def convertCellToPixel(self, (x, y)):
		""" Return a tuple with pixel positions."""
		return np.array((x * SCREEN_DIM[0], y * SCREEN_DIM[1]))

	def loadMap(self, filename):
		"""
		Load a map.
		Update attributes: mapName, txtMap, hero_*_x, hero_*_y, lCoordTreasure, lCoordTrap, width and height
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
		
		self.hero_pixel_x, self.hero_pixel_y = self.convertCellToPixel([self.hero_cell_x, self.hero_cell_y])

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
				hero     = True if (i,j) == (self.hero_cell_x, self.hero_cell_y) else False
				treasure = True if (i,j) in self.lCoordTreasure else False
				trap     = True if (i,j) in self.lCoordTrap else False
				self.cellMap[i].append( Cell(surface, j, i, self.hero_cell_x, self.hero_cell_y, hero, treasure, trap) )

	def decodeMapCell(self, code):
		""" Decode a map's cell."""
		return {'w':"water", 'f':"forest", 'p':"path", 'n':"none", 'W':"wall"}[code]

	def getCellSprites(self, (hero_cell_x, hero_cell_y)):
		""" Return all the cell.sprite attributes withing the range of the hero.
		'hero_cell_x': hero cell position
		'hero_cell_y': hero cell position
		"""
		lSprite = []
		for i in xrange(hero_cell_y - SCREEN_DIM[1]/2 -1, hero_cell_y + SCREEN_DIM[1]/2 +1):
			for j in xrange(hero_cell_x - SCREEN_DIM[0]/2 -1, hero_cell_x + SCREEN_DIM[0]/2 +1):
				if i < 0 or i >= self.height: continue
				if j < 0 or j >= self.width: continue
				lSprite.append( self.cellMap[i][j].sprite )
		return lSprite

	def getCellBorder(self, (hero_cell_x, hero_cell_y), flank=0):
		""" Return a list of tuples, corresponding to the position of each cells on the border of the map."""
		xleft = hero_cell_x - SCREEN_DIM[0]/2 - flank
		xright = hero_cell_x + SCREEN_DIM[0]/2 + flank
		ytop = hero_cell_y - SCREEN_DIM[0]/2 - flank
		ybot = hero_cell_y + SCREEN_DIM[0]/2 + flank
		
		border = zip(range(xleft, xright+1), [ytop]*(xright-xleft+1)) # top
		border.extend( zip(range(xleft, xright+1), [ybot]*(xright-xleft+1)) ) # bot
		border.extend( zip([xleft]*(ybot-ytop+1), range(ytop+1, ybot)) ) # left
		border.extend( zip([xright]*(ybot-ytop+1), range(ytop+1, ybot)) ) # right
		return border


