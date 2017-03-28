#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

import os,sys
import time
import src.JsonParser as JsonParser
import random as rd
import pygame

import src.Utility.Utils as Utils

from src.Cell import Cell
from src.Hero import Hero
from src.Item import Item
from src.Monster import Monster
from src.Spell import Spell
from src.World import World

import src.Graphic
import src.Utility.Colors as Colors

if __name__=='__main__':
	print Utils.ROOT_DIR
	print Utils.IMAGE_PATH
	print Utils.JSON_PATH
	print Utils.MAP_PATH
	## ======================================
	## Initialize Pygame and an 800*600 sized screen
	## ======================================
	pygame.init()
	screen_size = [800, 600]
	screen = pygame.display.set_mode(screen_size)
	
	# Used to manage how fast the screen updates
	clock = pygame.time.Clock()
	
	# Ending flag
	endflag = False
	
	n = 0
	colorKey = sorted(pygame.color.THECOLORS.keys())
	SPEED = 3
	
	# Init list of sprites
	all_sprites_list = pygame.sprite.Group()
	
	## ======================================
	## Load data
	## ======================================
	# JSON file: Hero, Monster, Item, Spell
	defaultDataFile = os.sep.join([Utils.ROOT_DIR, "data", "json", "default.json"])
	jsonData = JsonParser.loadJSON( defaultDataFile )
	dObj = {}
	for Class in [Hero, Monster, Item, Spell]:
		dObj.update( JsonParser.readObject(jsonData, Class) )
	
	all_sprites_list.add(dObj['h1'].sprite)
	
	# Map
	world = World()
	world.loadMap(os.sep.join([Utils.MAP_PATH, os.sep, "default.txt"]))
	cellMap = world.cellulizeMap("Default map")
	
	## ======================================
	## Main program loop
	## ======================================
	while not endflag:
		# Parse all event done by the user
		for event in pygame.event.get():
#			print event
			if event.type == pygame.QUIT:
				endflag = True
			
			elif event.type == pygame.MOUSEMOTION:
				n = (n+1)%len(colorKey)
				print colorKey[n]
			
			# Set the speed based on the key pressed
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					dObj['h1'].sprite.preUpdate(-SPEED, 0, "left")
				elif event.key == pygame.K_RIGHT:
					dObj['h1'].sprite.preUpdate(SPEED, 0, "right")
				elif event.key == pygame.K_UP:
					dObj['h1'].sprite.preUpdate(0, -SPEED, "up")
				elif event.key == pygame.K_DOWN:
					dObj['h1'].sprite.preUpdate(0, SPEED, "down")
	 
			# Reset speed when key goes up
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					dObj['h1'].sprite.preUpdate(SPEED, 0, "left")
				elif event.key == pygame.K_RIGHT:
					dObj['h1'].sprite.preUpdate(-SPEED, 0, "right")
				elif event.key == pygame.K_UP:
					dObj['h1'].sprite.preUpdate(0, SPEED, "up")
				elif event.key == pygame.K_DOWN:
					dObj['h1'].sprite.preUpdate(0, -SPEED, "down")
		
		## ==================================
		## Draw section
		## ==================================
		
		# Update sprites
		all_sprites_list.update()
		
		# Clear screen
		screen.fill( pygame.color.THECOLORS[colorKey[n]] )
		
		# Draw sprites
		all_sprites_list.draw(screen)
		
		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()
		
		# Limit to 60 frames per second
		clock.tick(60)
	# End while
	pygame.quit()
	
	
	
	
	
	
	
	
	
	
	 
	
	
	
	
	
	
	
	
	
	
