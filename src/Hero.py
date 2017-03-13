#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 12 Mar 2017

import os,sys

class Hero():
	"""
	All informations and stuff about the hero.
	"""
	def __init__(self, ID, name, race, gender, age):
		self.id = ID
		## Social caracteristics
		self.name = name
		self.race = race
		self.gender = gender
		self.age = age
		
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

