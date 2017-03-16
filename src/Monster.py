#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

class Monster():
	"""
	Object representing a monster.
	"""
	def __init__(self, **kwargs):
		## --- Set default Monster attributes
		self.id = 'm0'
		## Social caracteristics
		self.name = "Gobelin"
		self.type = "Beast" # Human, Undead, Beast, ...
		self.gender = "Male"
		
		## Stats
		self.health = 100
		self.experience = 0
		self.level = 1
		
		self.armor = 0
		self.dResistances = {"fire": 0, "lightning": 0, "cold": 0}
		
		self.baseDamage = 5
		self.critic = 0.05
		
		# Loot
		self.loots = {'item': 0.05}
		
		## --- Set users attributes
		for k,v in kwargs.items():
			if hasattr(self, k): setattr(self, k, v)
			else: print "\033[1;31mError\033[0m: the attribute {} doesn\'t exist.".format(k)

	def __repr__(self):
		txt = "[ %s ] %s level %d." %(self.name, self.type, self.level)
		return txt
