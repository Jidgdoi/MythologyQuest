#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

class Cell():
	"""
	Object representing a single Cell in the entire flat world.
	"""
	water = 47
	def __init__(self, x, y, Type):
		self.x = x
		self.y = y
		self.type = Type
		self.hero = False
		self.treasure = False
		self.trap = False
	
	def isWalkable(self):
		return True if self.type not in ['wall', 'water'] else False
