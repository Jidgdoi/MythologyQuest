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
	fpstime = 0
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
	world = World(os.sep.join([Utils.MAP_PATH, "three_cities.map"]))
	
	print "World cell dimension: {}".format((world.width, world.height))
	
	# Hero
	hero_cell_position = world.get_initial_hero_pos()
	hero_pixel_position = world.convertCellToPixel(hero_cell_position)
	hero_shift = np.array([0, 0]) # Pixel movement
	
	# Screen
	screen_corner = world.screenCornerPos(hero_cell_position)
	
	# Cell sprites
	lSprites_cell.add( world.getCellSprites(screen_corner) )
	
	# Text font
	pygame.font.init()
	myfont = pygame.font.SysFont('Comic Sans MS', 15)
	
	## ======================================
	## Main program loop
	## ======================================
	while not endflag:
		## ==================================
		## Event section
		## ==================================
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				endflag = True
			
			# Set the speed based on the key pressed
			elif event.type == pygame.KEYDOWN:
				## Movement
				if event.key == pygame.K_LEFT:
					dObj['h1'].sprite.preUpdateImg("left")
					hero_shift += (-Utils.HERO_SPEED, 0)
				elif event.key == pygame.K_RIGHT:
					dObj['h1'].sprite.preUpdateImg("right")
					hero_shift += (Utils.HERO_SPEED, 0)
				elif event.key == pygame.K_UP:
					dObj['h1'].sprite.preUpdateImg("up")
					hero_shift += (0, -Utils.HERO_SPEED)
				elif event.key == pygame.K_DOWN:
					dObj['h1'].sprite.preUpdateImg("down")
					hero_shift += (0, Utils.HERO_SPEED)
				## Menu and Options
				elif event.key == pygame.K_q:
					endflag = True
			
			# Reset speed when key goes up
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					hero_shift += (Utils.HERO_SPEED, 0)
				elif event.key == pygame.K_RIGHT:
					hero_shift += (-Utils.HERO_SPEED, 0)
				elif event.key == pygame.K_UP:
					hero_shift += (0, Utils.HERO_SPEED)
				elif event.key == pygame.K_DOWN:
					hero_shift += (0, -Utils.HERO_SPEED)
		
		## Update hero position
		hero_pixel_position += hero_shift
		hero_cell_position = world.convertPixelToCell(hero_pixel_position)
		
		## Check for collision, and therefore re-update hero position
#		lSpriteAroundHero = world.getSpriteAroundHero(hero_cell_position)
#		print len(lSpriteAroundHero)
		
		# Update screen position according hero position
		screen_corner = world.screenCornerPos(hero_cell_position)
		screen_pixel_corner = world.screenCornerPos(hero_pixel_position, True)
		screen_pixel_shift = hero_pixel_position%Utils.CELL_DIM
		
		if fpstime%60 == 0:
			print "Hero pixel:", hero_pixel_position, "\tHero cell:", hero_cell_position, "\tScreen corner:", screen_corner, "\tScreen pxl shift:", screen_pixel_shift
		
		## ==================================
		## Draw section
		## ==================================
		
		## Update sprites list
		borderRemove = world.getCellBorder(screen_corner, 2)
		borderAdd = world.getCellBorder(screen_corner, 0) + world.getCellBorder(screen_corner, 1)
		
		for sprite in lSprites_cell:
			if sprite.xy in borderRemove:
				lSprites_cell.remove(sprite)
		
		for (x,y) in borderAdd:
			if (x < 0 or x >= world.width) or (y < 0 or y >= world.height): continue
			if not lSprites_cell.has( world.cellMap[x][y].sprite ):
				world.cellMap[x][y].sprite.enterTheGame( screen_pixel_corner )
				lSprites_cell.add( world.cellMap[x][y].sprite )
		
		lSprites_hero.update()
		lSprites_cell.update(hero_shift)
		
		## Clear screen
		screen.fill( Utils.COLORS['water'] )
		
		## Draw sprites
		lSprites_cell.draw(screen)
		lSprites_hero.draw(screen)
		
		## Draw rows and columns number
		for i in xrange(screen_corner[1], screen_corner[1] + Utils.SCREEN_DIM[1]):
			for j in xrange(screen_corner[0], screen_corner[0] + Utils.SCREEN_DIM[0]):
				text = myfont.render("%d/%d" %(j,i), True, (0, 0, 0))
				screen.blit(text, world.convertCellToPixel( (j,i) - screen_corner ))
		
		## Go ahead and update the screen with what we've drawn.
		pygame.display.flip()
		
		## Limit to X frames per second (default 60)
		clock.tick(Utils.FPS)
		
		fpstime = (fpstime+1)%60
	
	# End while
	pygame.quit()





