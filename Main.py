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

from src.Cell import Cell,Cell_both
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
	
	sprite_hero = dObj['h1'].sprite
	lSprites_hero.add(sprite_hero)
	
	# World map
	world = World(os.sep.join([Utils.MAP_PATH, "three_cities.map"]))
	
	print "World cell dimension: {}".format((world.width, world.height))
	
	# Hero
	hero_shift = np.array([0, 0]) # Pixel movement
	
	# Screen
	screen_cell_corner = world.getScreenCornerPos(world.hero_cell_xy, pixel=False)
	screen_pixel_corner = world.getScreenCornerPos(world.hero_pixel_xy, pixel=True)
	
	# Cell sprites
	lSprites_cell.add( world.getCellSprites(screen_cell_corner) )
	
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
					hero_shift += (+Utils.HERO_SPEED, 0)
				elif event.key == pygame.K_RIGHT:
					dObj['h1'].sprite.preUpdateImg("right")
					hero_shift += (-Utils.HERO_SPEED, 0)
				elif event.key == pygame.K_UP:
					dObj['h1'].sprite.preUpdateImg("up")
					hero_shift += (0, +Utils.HERO_SPEED)
				elif event.key == pygame.K_DOWN:
					dObj['h1'].sprite.preUpdateImg("down")
					hero_shift += (0, -Utils.HERO_SPEED)
				## Menu and Options
				elif event.key == pygame.K_q:
					endflag = True
			
			# Reset speed when key goes up
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					hero_shift += (-Utils.HERO_SPEED, 0)
				elif event.key == pygame.K_RIGHT:
					hero_shift += (+Utils.HERO_SPEED, 0)
				elif event.key == pygame.K_UP:
					hero_shift += (0, -Utils.HERO_SPEED)
				elif event.key == pygame.K_DOWN:
					hero_shift += (0, +Utils.HERO_SPEED)
		
		## Update hero cell and pixel positions and check for collision
		isHeroCollide = world.updateHeroPos(sprite_hero, hero_shift)
		
		# Update screen position according to hero position
		screen_pixel_corner = world.getScreenCornerPos(world.hero_pixel_xy, pixel=True)
		screen_cell_corner = world.convertPixelToCell(screen_pixel_corner)
		
		if fpstime%60 == 0:
			print "Hero pixel:", world.hero_pixel_xy, "\tHero cell:", world.hero_cell_xy, "\tScreen pxl corner:", screen_pixel_corner, "\tScreen cell corner:", screen_cell_corner
		
		## ==================================
		## Sprite section
		## ==================================
		
		## Update sprites list
		borderRemove = world.getCellBorderPos(screen_cell_corner, 2, torus=True)
		borderAdd = world.getCellBorderPos(screen_cell_corner, 1, torus=False)
		
		## Remove sprites on the border +2
		for sprite in lSprites_cell:
			if sprite.xy in borderRemove:
				borderRemove.remove(sprite.xy)
				lSprites_cell.remove(sprite)
		
		## Update sprites list
		lSprites_hero.update()
		lSprites_cell.update(hero_shift if not isHeroCollide else [0,0])
		
		## Add missing sprites on the border +1
		for (x,y) in borderAdd:
			xp, yp = x%world.width, y%world.height # Cell's position in the world array
			if not lSprites_cell.has( world.cellMap[xp][yp] ):
				world.cellMap[xp][yp].enterTheGame( screen_pixel_corner, (x,y) )
				lSprites_cell.add( world.cellMap[xp][yp] )
		
		## ==================================
		## Draw section
		## ==================================
		
		## Clear screen
		screen.fill( Utils.COLORS['water'] )
		
		## Draw sprites
		lSprites_cell.draw(screen)
		lSprites_hero.draw(screen)
		
		## Draw rows and columns number
		for i in xrange(screen_cell_corner[1], screen_cell_corner[1] + Utils.SCREEN_DIM[1]):
			for j in xrange(screen_cell_corner[0], screen_cell_corner[0] + Utils.SCREEN_DIM[0]):
				text = myfont.render("%d/%d" %(j,i), True, (70, 70, 70))
				text2 = myfont.render("(%d/%d)" %(j%world.width,i%world.height), True, (70, 70, 70))
				screen.blit(text, world.convertCellToPixel( (j,i) - screen_cell_corner ))
				screen.blit(text2, world.convertCellToPixel( (j,i) - screen_cell_corner ) + (0,15))
		
		## Go ahead and update the screen with what we've drawn.
		pygame.display.flip()
		
		## Limit to X frames per second (default 60)
		clock.tick(Utils.FPS)
		
		fpstime = (fpstime+1)%60
	
	# End while
	pygame.quit()





