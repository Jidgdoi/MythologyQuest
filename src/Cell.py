#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

import pygame
from src.Utility.Utils import CELL_DIM,SCREEN_DIM,COLORS

class Cell():
	"""
	Object representing a single Cell in the entire flat world.
	"""
	water = 47
	def __init__(self, surface, xy, hero_pixel_xy, hero=False, treasure=False, trap=False):
		self.surface = surface
		self.hero = hero
		self.treasure = treasure
		self.trap = trap
		self.item = hero if hero else treasure if treasure else trap if trap else ''
		
		self.isWalkable = True if self.surface not in ['wall', 'water'] else False
		self.isWaterway = True if self.surface == 'water' else False
		
		self.sprite = Cell_sprite(self.surface, xy, hero_pixel_xy)

	def __repr__(self):
		txt = "[ %s ]" %self.surface
		if self.hero: txt += " Hero: %s" %self.hero
		if self.treasure: txt += " Treasure: %s" %self.treasure
		if self.trap: txt += " Trap: %s" %self.trap
		return txt

	def update(self, **kwargs):
		"""
		Update an argument of the Cell.
		"""
		for k,v in kwargs.items():
			if hasattr(self, k): setattr(self, k, v)
			else: print "\033[1;31mError\033[0m: the attribute {} doesn\'t exist.".format(k)

class Cell_sprite(pygame.sprite.Sprite):
	"""
	This class represents a Cell in graphic mode.
	It derives from the "Sprite" class in Pygame.
	"""
	def __init__(self, surface, xy, hero_pixel_xy):
		# Call the parent class (Sprite) constructor
		super(Cell_sprite, self).__init__() 
		
		# Cell position in the array
		self.xy = xy
		
		# Set height, width
		self.image = pygame.Surface(CELL_DIM)
		self.image.fill( COLORS[surface] )
		
		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.x,self.rect.y = self.xy*CELL_DIM - hero_pixel_xy

	def enterTheGame(self, screen_pixel_corner_xy, xy_real):
		""" The sprite is in range of the hero: set his position on the screen.
		'screen_pixel_corner_xy': screen corner position in pixel units
		'xy_real': cell position on the real screen (self.xy are cell position in the wolrd array)
		"""
		self.rect.x,self.rect.y = xy_real*CELL_DIM - screen_pixel_corner_xy

	def update(self, (hero_shift_x, hero_shift_y)):
		""" Called by the Group sprite function Update(*args), update position of the cell.
		'(hero_shift_x, hero_shift_y)': tuple of pixel shift on x and y axis
		"""
		self.rect.x -= hero_shift_x
		self.rect.y -= hero_shift_y

class Cell_both(pygame.sprite.Sprite):
	"""
	This class represents a Cell in graphic mode.
	It derives from the "Sprite" class in Pygame.
	"""
	water = 47
	def __init__(self, surface, xy, hero_pixel_xy, hero=False, treasure=False, trap=False):
		# Call the parent class (Sprite) constructor
		super(Cell_both, self).__init__()
		
		# Cell position in the array
		self.xy = xy
		
		# Set height, width
		self.image = pygame.Surface(CELL_DIM)
		self.image.fill( COLORS[surface] )
		
		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.x,self.rect.y = self.xy*CELL_DIM - hero_pixel_xy
		
		# Cell parameters
		self.surface = surface
		self.hero = hero
		self.treasure = treasure
		self.trap = trap
		self.item = hero if hero else treasure if treasure else trap if trap else ''
		
		self.isWalkable = True if self.surface not in ['wall', 'water'] else False
		self.isWaterway = True if self.surface == 'water' else False

	def __repr__(self):
		txt = "[ %s ]" %self.surface
		if self.hero: txt += " Hero: %s" %self.hero
		if self.treasure: txt += " Treasure: %s" %self.treasure
		if self.trap: txt += " Trap: %s" %self.trap
		return txt

	def updateArgs(self, **kwargs):
		"""
		Update an argument of the Cell.
		"""
		for k,v in kwargs.items():
			if hasattr(self, k): setattr(self, k, v)
			else: print "\033[1;31mError\033[0m: the attribute {} doesn\'t exist.".format(k)

	def enterTheGame(self, screen_pixel_corner_xy, xy_real):
		""" The sprite is in range of the hero: set his position on the screen.
		'screen_pixel_corner_xy': screen corner position in pixel units
		'xy_real': cell position on the real screen (self.xy are cell position in the wolrd array)
		"""
		self.rect.x,self.rect.y = xy_real*CELL_DIM - screen_pixel_corner_xy

	def update(self, (hero_shift_x, hero_shift_y)):
		""" Called by the Group sprite function Update(*args), update position of the cell.
		'(hero_shift_x, hero_shift_y)': tuple of pixel shift on x and y axis
		"""
		self.rect.x += hero_shift_x
		self.rect.y += hero_shift_y
