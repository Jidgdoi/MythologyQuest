#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

class Cell():
	"""
	Object representing a single Cell in the entire flat world.
	"""
	water = 47
	def __init__(self, x, y, surface, **kwargs):
		self.x = x
		self.y = y
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
		
		self.design = self.terminalDesign()

	def __repr__(self):
		return self.design

	def terminalDesign(self):
		"""
		Return the design of the cell to print in a terminal.
		"""
		## Set background
		bg = ''
		if self.surface == "water": bg = 44
		elif self.surface == "forest": bg = 42
		elif self.surface == "path": tbg = 47
		## Set foreground
		fg = '39'
		effect = ''
		icon = ' '
		if self.hero: fg = 31; effect = 1; icon = "H"
		elif self.treasure: fg = 33; effect = 1; icon = "T"
		elif self.trap: fg = 35; effect = 3; icon = "^"
		
		return "\033[%s;%s;%sm%s\033[0m" %(effect, bg, fg, icon)

	def update(self, **kwargs):
		"""
		Update an argument of the Cell.
		"""
		for k,v in kwargs.items():
			if hasattr(self, k): setattr(self, k, v)
			else: print "\033[1;31mError\033[0m: the attribute {} doesn\'t exist.".format(k)
		self.design = self.terminalDesign()




