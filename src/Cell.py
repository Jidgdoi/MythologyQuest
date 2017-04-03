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
	def __init__(self, surface, x, y, hero_x, hero_y, hero=False, treasure=False, trap=False):
		self.surface = surface
		self.hero = hero
		self.treasure = treasure
		self.trap = trap
		self.item = hero if hero else treasure if treasure else trap if trap else ''
		
		self.isWalkable = True if self.surface not in ['wall', 'water'] else False
		self.isWaterway = True if self.surface == 'water' else False
		
		self.sprite = Cell_sprite(self.surface, x, y, hero_x, hero_y)

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
	def __init__(self, surface, x, y, hero_x, hero_y):
		# Call the parent class (Sprite) constructor
		super(Cell_sprite, self).__init__() 
		
		# Set height, width
		self.image = pygame.Surface(CELL_DIM)
		self.image.fill( COLORS[surface] )
		
		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.x = (x - hero_x + SCREEN_DIM[0]/2) * self.rect.width
		self.rect.y = (y - hero_y + SCREEN_DIM[1]/2) * self.rect.height
		
		# Hero position
		self.hero_x = hero_x
		self.hero_y = hero_y
		
		# Hero movement
		self.change_x = 0
		self.change_y = 0

	def changePos(self, x, y):
		self.change_x += x
		self.change_y += y

	def update(self):
		self.rect.x += self.change_x
		self.rect.y += self.change_y

	def reset(self):
		self.change_x = 0
		self.change_y = 0
