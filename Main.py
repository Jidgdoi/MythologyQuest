#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

import os,sys
import time
import src.JsonParser as JsonParser
import random as rd
import numpy as np
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
	
	# World map
	world = World(os.sep.join([Utils.MAP_PATH, "default.map"]))
	
	# Hero
	hero_cell_position = world.get_hero_pos()
	hero_pixel_position = world.convertCellToPixel(hero_cell_position)
	hero_moving = np.array([0, 0]) # Pixel movement
	
	# Cell sprites
	lSprites_cell.add( world.getCellSprites(hero_cell_position) )
	
	## ======================================
	## Main program loop
	## ======================================
	while not endflag:
		# Parse all event done by the user
		for event in pygame.event.get():
			print "Hero cell position:", hero_cell_position, "\tHero pixel position:", hero_pixel_position
			if event.type == pygame.QUIT:
				endflag = True
			
			# Set the speed based on the key pressed
			elif event.type == pygame.KEYDOWN:
				## Movement
				if event.key == pygame.K_LEFT:
					dObj['h1'].sprite.preUpdateImg("left")
					hero_moving += (Utils.SPEED, 0)
				elif event.key == pygame.K_RIGHT:
					dObj['h1'].sprite.preUpdateImg("right")
					hero_moving += (-Utils.SPEED, 0)
				elif event.key == pygame.K_UP:
					dObj['h1'].sprite.preUpdateImg("up")
					hero_moving += (0, Utils.SPEED)
				elif event.key == pygame.K_DOWN:
					dObj['h1'].sprite.preUpdateImg("down")
					hero_moving += (0, -Utils.SPEED)
				## Menu and Options
				elif event.key == pygame.K_q:
					endflag = True
			
			# Reset speed when key goes up
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					dObj['h1'].sprite.preUpdateImg("left")
					hero_moving += (-Utils.SPEED, 0)
				elif event.key == pygame.K_RIGHT:
					dObj['h1'].sprite.preUpdateImg("right")
					hero_moving += (Utils.SPEED, 0)
				elif event.key == pygame.K_UP:
					dObj['h1'].sprite.preUpdateImg("up")
					hero_moving += (0, -Utils.SPEED)
				elif event.key == pygame.K_DOWN:
					dObj['h1'].sprite.preUpdateImg("down")
					hero_moving += (0, Utils.SPEED)
		
		## ==================================
		## Draw section
		## ==================================
		# Update hero position
		hero_pixel_position += hero_moving
		hero_cell_position = world.convertPixelToCell(hero_pixel_position)
		
		# Update sprites list
		## Only ones in border
		### top
		borderAdd = world.getCellBorder(hero_cell_position, 1)
		borderRemove = world.getCellBorder(hero_cell_position, 2)
		
		print "[1]Nb sprites:", len(lSprites_cell)
		for sprite in lSprites_cell:
			if (sprite.x, sprite.y) in borderRemove:
				lSprites_cell.remove(sprite)
		print "[2]Nb sprites:", len(lSprites_cell)
		
		for (x,y) in borderAdd:
			if x < 0 or x >= world.height: continue
			if y < 0 or y >= world.width: continue
			if not lSprites_cell.has( world.cellMap[y][x].sprite ):
				lSprites_cell.add( world.cellMap[y][x].sprite )
		print "[3]Nb sprites:", len(lSprites_cell)
		
		lSprites_hero.update()
		lSprites_cell.update(hero_pixel_position)
		
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
	
	
	
	
	
	
	
	
