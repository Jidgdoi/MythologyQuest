#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

import os,sys
import time
import src.JsonParser as JsonParser
import random as rd
import pygame
from itertools import chain

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
	## ======================================
	## Initialize Pygame and an 800*600 sized screen
	## ======================================
	pygame.init()
	screen = pygame.display.set_mode( Utils.SCREEN_SIZE)
	
	# Used to manage how fast the screen updates
	clock = pygame.time.Clock()
	
	# Ending flag
	endflag = False
	
	# Init list of sprites
	lSprites_hero = pygame.sprite.Group()
	lSprites_cell = pygame.sprite.Group()
	
	## ======================================
	## Load data
	## ======================================
	# JSON file: Hero, Monster, Item, Spell
	defaultDataFile = os.sep.join([Utils.ROOT_DIR, "data", "json", "default.json"])
	jsonData = JsonParser.loadJSON( defaultDataFile )
	dObj = {}
	for Class in [Hero, Monster, Item, Spell]:
		dObj.update( JsonParser.readObject(jsonData, Class) )
	
	lSprites_hero.add(dObj['h1'].sprite)
	
	# Map
	world = World(os.sep.join([Utils.MAP_PATH, "default.map"]))
	
	lSprites_cell.add( world.getCellSprites() )
	
	## ======================================
	## Main program loop
	## ======================================
	while not endflag:
		# Parse all event done by the user
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				endflag = True
			
			# Set the speed based on the key pressed
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					dObj['h1'].sprite.preUpdate("left")
					[cell_sprite.changePos(Utils.SPEED, 0) for cell_sprite in lSprites_cell]
				elif event.key == pygame.K_RIGHT:
					dObj['h1'].sprite.preUpdate("right")
					[cell_sprite.changePos(-Utils.SPEED, 0) for cell_sprite in lSprites_cell]
				elif event.key == pygame.K_UP:
					dObj['h1'].sprite.preUpdate("up")
					[cell_sprite.changePos(0, Utils.SPEED) for cell_sprite in lSprites_cell]
				elif event.key == pygame.K_DOWN:
					dObj['h1'].sprite.preUpdate("down")
					[cell_sprite.changePos(0, -Utils.SPEED) for cell_sprite in lSprites_cell]
			
			# Reset speed when key goes up
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					dObj['h1'].sprite.preUpdate("left")
					[cell_sprite.changePos(-Utils.SPEED, 0) for cell_sprite in lSprites_cell]
				elif event.key == pygame.K_RIGHT:
					dObj['h1'].sprite.preUpdate("right")
					[cell_sprite.changePos(Utils.SPEED, 0) for cell_sprite in lSprites_cell]
				elif event.key == pygame.K_UP:
					dObj['h1'].sprite.preUpdate("up")
					[cell_sprite.changePos(0, -Utils.SPEED) for cell_sprite in lSprites_cell]
				elif event.key == pygame.K_DOWN:
					dObj['h1'].sprite.preUpdate("down")
					[cell_sprite.changePos(0, Utils.SPEED) for cell_sprite in lSprites_cell]
		
		## ==================================
		## Draw section
		## ==================================
		
		# Update sprites
		lSprites_hero.update()
		lSprites_cell.update()
		
		# Clear screen
		screen.fill( Utils.COLORS['water'] )
		
		# Draw sprites
		lSprites_cell.draw(screen)
		lSprites_hero.draw(screen)
		
		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()
		
		# Limit to 60 frames per second
		clock.tick(60)
	# End while
	pygame.quit()
	
	
	
	
	
	
	
	
	
	
	 
	
	
	
	
	
	
	
	
	
	
