#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

import pygame
import numpy as np

from Cell import Cell
from collections import defaultdict,deque
import src.JsonParser as JsonParser

from src.Utility.Utils import SCREEN_DIM,CELL_DIM,SCREEN_SIZE

class World():
	"""
	Object representing the entire flat world.
	"""
	def __init__(self, filename):
		self.mapName = "default"
		## Attributes storing map
		self.cellMap = defaultdict(lambda: defaultdict(str))
		self.sprites = pygame.sprite.Group()
		## Map cell dimension
		self.width = 0
		self.height = 0
		## Hero position
		self.hero_cell_xy = np.array([0,0])
		self.hero_pixel_xy = np.array([0,0])
		## Treasure and trap coordinates
		self.lCoordTreasure = []
		self.lCoordTrap = []
		
		## Load and create map
		self.loadMap(filename)

	def get_initial_hero_pos(self):
		return self.hero_cell_xy

	def convertPixelToCell(self, (x, y)):
		""" Return a tuple with cell positions.
		'(x, y)': Pixel position of the hero.
		"""
		return np.array((x / CELL_DIM[0], y / CELL_DIM[1]))

	def convertCellToPixel(self, (x, y)):
		""" Return a tuple with pixel positions.
		'(x, y)': Cell position of the hero.
		"""
		return np.array((x * CELL_DIM[0], y * CELL_DIM[1]))

	def screenCornerPos(self, (x, y), pixel=False):
		""" Return the top left corner of the screen centered on the hero, means (0,0).
		'(x, y)': Position of the hero (cell or pixel).
		'pixel': Boolean to treat pixel instead of cell postion.
		"""
		if pixel: return np.array((x - SCREEN_SIZE[0]/2, y - SCREEN_SIZE[1]/2))
		return np.array((x - SCREEN_DIM[0]/2, y - SCREEN_DIM[1]/2))

	def loadMap(self, filename):
		"""
		Load a map.
		Update attributes: mapName, txtMap, hero_*_x, hero_*_y, lCoordTreasure, lCoordTrap, width and height
		'filename': map filename.
		"""
		untreatedMap = deque()
		## Open map file
		fh = open(filename, 'r')
		## Read map part of file
		line = fh.readline()
		while line != '\n':
			untreatedMap.append( deque(line.strip().split(';')) )
			line = fh.readline()
		
		## Read JSON content's part of file
		content = JsonParser.loadJSONmap(fh)
		
		fh.close()
		
		## Set attributes
		self.width = len(untreatedMap[0])
		self.height = len(untreatedMap)
		
		for k,v in content['Map'].items():
			if hasattr(self, k): setattr(self, k, v)
			else: print "\033[1;31mError\033[0m: the attribute '{}' doesn\'t exist.".format(k)
		self.hero_cell_xy = np.array(self.hero_cell_xy)
		self.hero_pixel_xy = self.convertCellToPixel(self.hero_cell_xy)
		
		## Cellulize map
		self.cellulizeMap(untreatedMap)

	def cellulizeMap(self, untreatedMap):
		"""
		Cellulize a map, which means create the map with Cell objects.
		Update attribute cellMap.
		"""
		for y in xrange(self.height):
			for x in xrange(self.width):
				surface = self.decodeMapCell(untreatedMap[y][x])
				hero     = True if ((x,y) == self.hero_cell_xy).all() else False
				treasure = True if (x,y) in self.lCoordTreasure else False
				trap     = True if (x,y) in self.lCoordTrap else False
				self.cellMap[x][y] = Cell(surface, (x, y), self.screenCornerPos(self.hero_pixel_xy, True), hero, treasure, trap)

	def decodeMapCell(self, code):
		""" Decode a map's cell."""
		return {'w':"water", 'f':"forest", 'p':"path", 'n':"none", 'W':"wall"}[code]

	def getCellSprites(self, (screen_corner_x, screen_corner_y)):
		""" Return all the cell.sprite attributes withing the range of the hero.
		'hero_cell_x': hero cell position
		'hero_cell_y': hero cell position
		"""
		lSprite = []
		for x in xrange(screen_corner_x -1, screen_corner_x + SCREEN_DIM[0] +1):
			for y in xrange(screen_corner_y -1, screen_corner_y + SCREEN_DIM[1] +1):
				if (x < 0 or x >= self.width) or (y < 0 or y >= self.height): continue
				lSprite.append( self.cellMap[x][y].sprite )
		return lSprite

	def getCellBorder(self, (screen_corner_x, screen_corner_y), flank=0):
		""" Return a list of tuples, corresponding to the position of each cells on the border of the map."""
		xleft = screen_corner_x - flank
		xright = screen_corner_x + SCREEN_DIM[0] + flank
		ytop = screen_corner_y - flank
		ybot = screen_corner_y + SCREEN_DIM[1] -1 + flank
		
#		print "Flank: %d" %flank
#		print " Topleft: %s\tTopright: %s" %(zip(range(xleft, xright), [ytop]*(xright-xleft))[0], zip(range(xleft, xright), [ytop]*(xright-xleft))[-1])
#		print " Botleft: %s\tBotright: %s" %(zip(range(xleft, xright), [ybot]*(xright-xleft))[0], zip(range(xleft, xright), [ybot]*(xright-xleft))[-1])
		
		border = zip(range(xleft, xright), [ytop]*(xright-xleft)) # top
		border.extend( zip(range(xleft, xright), [ybot]*(xright-xleft)) ) # bot
		border.extend( zip([xleft]*(ybot-ytop), range(ytop, ybot)) ) # left
		border.extend( zip([xright]*(ybot-ytop), range(ytop, ybot)) ) # right
		return border


