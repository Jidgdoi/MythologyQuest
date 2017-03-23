#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 22 Mar 2017

import Utility.Colors as Colors

def terminalOutput(cellMap):
	"""
	Print map on Terminal output.
	"""
	## Colors associated to each features.
	dColor = {}
	for s in ("water", "forest", "path"):
		bg = "blue" if s == "water" else "green" if s == "forest" else ""
		for i in ("hero", "treasure", "trap", ""):
			t = "H" if i == "hero" else "T" if i == "treasure" else "^" if i == "trap" else " "
			dColor[(s,i)] = Colors.color(fgColor="red",bgColor=bg)(t)
	
	txt = ''
	for line in cellMap:
		previousCellType = False
		for cell in line:
			if previousCellType:
				# Space between 2 walls: set features wall for the space
				if cell.surface == "path": txt += dColor[(cell.surface,cell.item)]
				elif previousCellType == "path": txt += dColor[(cell.surface,cell.item)]
				elif previousCellType == cell.surface: txt += dColor[(cell.surface,cell.item)]
				elif previousCellType != cell.surface: txt += dColor[(cell.surface,cell.item)]
				# Just a space
				else: txt += ' '
			txt += dColor[(cell.surface,cell.item)]
			previousCellType = dColor[(cell.surface,cell.item)]
		txt += '\n'
	return txt

