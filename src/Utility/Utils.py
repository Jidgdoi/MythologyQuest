#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 28 Mar 2017

import os
import numpy as np

## Path utils
ROOT_DIR = os.sep.join(os.path.realpath(__file__).split(os.sep)[:-3])
IMAGE_PATH = os.sep.join([ROOT_DIR, "data", "image"])
JSON_PATH = os.sep.join([ROOT_DIR, "data", "json"])
MAP_PATH = os.sep.join([ROOT_DIR, "data", "map"])

## Cell utils
CELL_DIM = np.array( [20, 20] )

## Screen utils
SCREEN_SIZE = np.array( [800, 600] )
SCREEN_DIM = np.array( SCREEN_SIZE / CELL_DIM )

print SCREEN_DIM

## World utils
SPEED = CELL_DIM[0]/10

## Colors
COLORS = {'forest': (33, 198, 75),
		  'water' : (42, 182, 221),
		  'path'  : (152, 151, 163)}
