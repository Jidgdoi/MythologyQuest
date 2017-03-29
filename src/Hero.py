#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 12 Mar 2017

import os,sys
import pygame
from Utility.Utils import IMAGE_PATH,SCREEN_SIZE,CELL_DIM

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
		self.grade = "Unknown"
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
		
		## Graphics
		self.sprite = {}

	def __repr__(self):
		txt = "[ %s ] %s %s level %d." %(self.name, self.race, self.grade, self.level)
		return txt

	def __generateID__(self):
		"""Generate ID."""
		Hero.nextID += 1
		return "h%d"%Hero.nextID

	def activeSprite(self):
		"""Set the sprite attribute with the class Hero_sprite"""
		self.sprite = Hero_sprite(self.grade)

class Hero_sprite(pygame.sprite.Sprite):
	"""
	This class represents the hero in graphic mode.
	It derives from the "Sprite" class in Pygame.
	"""
	def __init__(self, grade):
		# Call the parent class (Sprite) constructor
		super(Hero_sprite, self).__init__() 
		
		# Load images of each position
		self.filename    = "%s%s%s_%%s.png" %(IMAGE_PATH, os.sep, grade)
		self.image_left  = pygame.image.load(self.filename %"left").convert()
		self.image_left  = pygame.transform.scale(self.image_left, CELL_DIM)
		self.image_right = pygame.image.load(self.filename %"right").convert()
		self.image_right  = pygame.transform.scale(self.image_right, CELL_DIM)
		self.image_up	 = pygame.image.load(self.filename %"up").convert()
		self.image_up  = pygame.transform.scale(self.image_up, CELL_DIM)
		self.image_down  = pygame.image.load(self.filename %"down").convert()
		self.image_down  = pygame.transform.scale(self.image_down, CELL_DIM)
		self.tmp_image   = self.image_down
		self.image       = self.tmp_image
		
		# Set background color
		self.image.set_colorkey((255, 255, 255))
		
		# Fetch the rectangle object that has the dimensions of the image
		# image.
		self.rect = self.image.get_rect()
		self.rect.x = SCREEN_SIZE[0]/2
		self.rect.y = SCREEN_SIZE[1]/2

	def preUpdate(self, state):
		"""Change the image profil of the character."""
		self.tmp_image = vars(self)["image_%s" %state]
 
	def update(self):
		"""Update the character's image."""
		self.image = self.tmp_image
