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

	def get_initial_hero_pos(self, pixel=True):
		""" Return hero initial position in pixel units or cell units.
		'pixel': set to True to return position in pixel units.
		"""
		return self.hero_pixel_xy if pixel else self.hero_cell_xy

	def convertPixelToCell(self, xy):
		""" Return a tuple with cell positions.
		'xy': Pixel position of the hero.
		"""
		return xy / CELL_DIM

	def convertCellToPixel(self, xy):
		""" Return a tuple with pixel positions.
		'xy': Cell position of the hero.
		"""
		return xy * CELL_DIM

	def getScreenCornerPos(self, xy, pixel=True):
		""" Return the top left corner of the screen centered on the hero, means (0,0).
		'xy': Position of the hero (cell or pixel).
		'pixel': Boolean to treat pixel instead of cell postion.
		"""
		if pixel: return xy - SCREEN_SIZE/2
		return xy - SCREEN_DIM/2

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
		self.hero_cell_xy = np.array(self.hero_cell_xy) # convert tuple to np.array
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
				self.cellMap[x][y] = Cell(surface, (x, y), self.getScreenCornerPos(self.hero_pixel_xy, True), hero, treasure, trap)

	def decodeMapCell(self, code):
		""" Decode a map's cell."""
		return {'w':"water", 'f':"forest", 'p':"path", 'n':"none", 'W':"wall", 'c':"city"}[code]

	def getCellSprites(self, (screen_corner_x, screen_corner_y)):
		""" Return all the cell's attribute 'sprite' within the screen limits.
		'(screen_corner_x, screen_corner_y)': screen corner position in cell units
		"""
		lSprite = []
		for x in xrange(screen_corner_x -1, screen_corner_x + SCREEN_DIM[0] +1):
			for y in xrange(screen_corner_y -1, screen_corner_y + SCREEN_DIM[1] +1):
				if (x < 0 or x >= self.width) or (y < 0 or y >= self.height): continue
				lSprite.append( self.cellMap[x][y] )
		return lSprite

	def getCellBorderPos(self, (cell_x, cell_y), flank=0, torus=True):
		""" Return a list of tuples, corresponding to the position of each cells on the border of the map.
		'(cell_x, cell_y)': screen corner position in cell units
		"""
		xleft = cell_x - flank
		xright = cell_x + SCREEN_DIM[0] + flank
		ytop = cell_y - flank
		ybot = cell_y + SCREEN_DIM[1] -1 + flank
		
#		print "## Flank:", flank
#		print "top:",  zip(range(xleft, xright), [ytop]*(xright-xleft))
#		print "bot",   zip(range(xleft, xright), [ybot]*(xright-xleft))
#		print "left",  zip([xleft]*(ybot-ytop), range(ytop+1, ybot))
#		print "right", zip([xright-1]*(ybot-ytop), range(ytop+1, ybot))
		
		border = zip(range(xleft, xright), [ytop]*(xright-xleft)) # top
		border.extend( zip(range(xleft, xright), [ybot]*(xright-xleft)) ) # bot
		border.extend( zip([xleft]*(ybot-ytop), range(ytop+1, ybot)) ) # left
		border.extend( zip([xright-1]*(ybot-ytop), range(ytop+1, ybot)) ) # right
		
		if torus:
			border = [(x%self.width, y%self.height) for (x,y) in border]
		return border

	def getSpriteAroundHero(self):
		""" Return the list of sprite object around the hero position."""
		lSprites = pygame.sprite.Group()
		for x in xrange(self.hero_cell_xy[0] -1, self.hero_cell_xy[0] +2):
			for y in xrange(self.hero_cell_xy[1] -1, self.hero_cell_xy[1] +2):
				if ((x,y) == self.hero_cell_xy).all(): continue
				lSprites.add( self.cellMap[x%self.width][y%self.height] )
		return lSprites

	def updateHeroPos(self, lSprites_hero, hero_shift):
		""" Check for collision between the hero and his environment."""
		lSprite = self.getSpriteAroundHero()
		collision = False
		
		## Move on x
		self.hero_pixel_xy[0] -= hero_shift[0]
		# Did this update cause us to hit a wall?
#		lBlockHit = pygame.sprite.spritecollide(lSprites_hero, lSprite, False)
#		for block in lBlockHit:
#			if not block.isWalkable:
#				collision = True
#				print "Block:", block.rect.x
#				print "Collision on x:", self.hero_pixel_xy[0]
#				self.hero_pixel_xy[0] = block.rect.left if hero_shift[0] > 0 else block.rect.right
#				print "End of collision:", self.hero_pixel_xy[0]
#		
		## Move on y
		
		self.hero_pixel_xy[1] -= hero_shift[1]
		# Check and see if we hit anything
#		lBlockHit = pygame.sprite.spritecollide(lSprites_hero, lSprite, False)
#		for block in lBlockHit:
#			if not block.isWalkable:
#				collision = True
#				print "Collision on y:", self.hero_pixel_xy[1]
#				self.hero_pixel_xy[1] = block.rect.top if hero_shift[1] > 0 else block.rect.bottom
#				print "End of collision:", self.hero_pixel_xy[1]
		
		self.hero_cell_xy = self.convertPixelToCell( self.hero_pixel_xy )
		
		return collision
		
