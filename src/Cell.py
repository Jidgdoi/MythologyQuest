#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

class Cell():
	"""
	Object representing a single Cell in the entire flat world.
	"""
	water = 47
	def __init__(self, surface, **kwargs):
		self.surface = surface
		self.hero = False
		self.treasure = False
		self.trap = False
		
		## --- Set users attributes
		for k,v in kwargs.items():
			if hasattr(self, k): setattr(self, k, v)
			else: print "\033[1;31mError\033[0m: the attribute {} doesn\'t exist.".format(k)
		
		self.isWalkable = True if self.surface not in ['wall', 'water'] else False
		self.isWaterway = True if self.surface == 'water' else False

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




