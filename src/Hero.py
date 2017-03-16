#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 12 Mar 2017

import os,sys

class Hero():
	"""
	All informations and stuff about the hero.
	"""
	def __init__(self, **kwargs):
		## --- Set default Hero attributes
		self.id = 'h0'
		## Social caracteristics
		self.name = "Unknown"
		self.race = "Human"
		self.grade = "Squire"
		self.gender = "Male"
		self.age = 20
		
		## Stats
		self.health = 100
		self.mana = 50
		self.experience = 0
		self.level = 1
		
		self.armor = 0
		self.dResistances = {"fire": 0, "lightning": 0, "cold": 0}
		
		self.baseDamage = 5
		self.critic = 0.05
		
		self.strength = 1
		self.agility = 1
		self.intelligence = 1
		self.vitality = 1
		
		## Stuff
		self.dStuff = {"head": None, "ears": None, "chest": None, "hands": None, "legs": None, "feet": None, "leftHand": None, "rightHand": None}
		self.bag = []
		
		## --- Set users attributes
		for k,v in kwargs.items():
			if hasattr(self, k): setattr(self, k, v)
			else: print "\033[1;31mError\033[0m: the attribute {} doesn\'t exist.".format(k)
	
	def __repr__(self):
		txt = "[ %s ] %s %s level %d." %(self.name, self.race, self.grade, self.level)
		return txt
