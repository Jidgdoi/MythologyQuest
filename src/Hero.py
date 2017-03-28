#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 12 Mar 2017

import os,sys
import pygame
from Utility.Utils import IMAGE_PATH

class Hero():
	"""
	All informations and stuff about the hero.
	"""
	nextID = 0
	def __init__(self, **kwargs):
		## --- Set default Hero attributes
		## Set ID
		self.id = self.__generateID__()
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
		
		## Graphics
		self.sprite = Hero_sprite(IMAGE_PATH, self.name)

	def __repr__(self):
		txt = "[ %s ] %s %s level %d." %(self.name, self.race, self.grade, self.level)
		return txt

	def __generateID__(self):
		"""
		Generate ID.
		"""
		Hero.nextID += 1
		return "h%d"%Hero.nextID

	def __updateSprite__(self):
		self.sprite = Hero_S

class Hero_sprite(pygame.sprite.Sprite):
	"""
	This class represents the hero in graphic mode.
	It derives from the "Sprite" class in Pygame.
	"""
	def __init__(self, imageDir, name):
		# Call the parent class (Sprite) constructor
		super(Hero_sprite, self).__init__() 
		
		# Create an image of the block, and fill it with a color.
		# This could also be an image loaded from the disk.
		filename = "%s%s%s_%%s.png" %(imageDir, os.sep, name)
		self.image_left  = pygame.image.load(filename %"left").convert()
		self.image_right = pygame.image.load(filename %"right").convert()
		self.image_up	= pygame.image.load(filename %"up").convert()
		self.image_down  = pygame.image.load(filename %"down").convert()
		self.default_image = self.image_down
		self.image = self.default_image
		
		# Set background color to be transparent. Adjust to WHITE if your
		# background is WHITE.
		self.image.set_colorkey((255, 255, 255, 0))
		
		# Fetch the rectangle object that has the dimensions of the image
		# image.
		# Update the position of this object by setting the values 
		# of rect.x and rect.y
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0
		
		# -- Attributes
		# Set speed vector
		self.change_x = 0
		self.change_y = 0

	def preUpdate(self, x, y, state):
		""" Change the speed of the player and his image"""
		self.change_x += x
		self.change_y += y
		self.default_image = vars(self)["image_%s" %state]
 
	def update(self):
		""" Find a new position for the player"""
		self.rect.x += self.change_x
		self.rect.y += self.change_y
		self.image = self.default_image
