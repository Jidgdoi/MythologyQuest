#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

class Monster():
	"""
	Object representing a monster.
	"""
	def __init__(self):
		self.id = ID
		## Social caracteristics
		self.name = name
		self.race = race # Human, Undead, Beast, ...
		self.gender = gender
		
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
