#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

import Cell

class World():
	"""
	Object representing the entire flat world.
	"""
	def __init__(self, height, width):
		self.height = height
		self.width = width
		self.world = self.createWorld(height, width)
	
	def createWorld(self, h, w):
		"""
		Return a nested list full of unset Cell.
		"""
		return [[Cell(x , y, 'grass') for y in range(w)] for x in range(h)]
		
