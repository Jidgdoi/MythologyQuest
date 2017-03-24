#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

import os,sys

class Spell():
	"""
	Description of a magical spell.
	"""
	nextID = 0
	def __init__(self, **kwargs):
		## --- Set default Item attributes
		self.id = self.__generateID__()
		self.name = "Spell"
		self.description = "Unset spell."
		self.type = "Unset" # Fire, Mystic, Dark, ...
		self.level = 0
		self.cost = 0
		self.action = {}
		
		## --- Set users attributes
		for k,v in kwargs.items():
			if hasattr(self, k): setattr(self, k, v)
			else: print "\033[1;31mError\033[0m: the attribute {} doesn\'t exist.".format(k)

	def __repr__(self):
		return "[ %s ] %s" %(self.name, self.description)

	def __generateID__(self):
		"""
		Generate ID.
		"""
		Spell.nextID += 1
		return "s%d"%Spell.nextID

