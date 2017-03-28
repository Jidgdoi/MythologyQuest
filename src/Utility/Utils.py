#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 28 Mar 2017

import os

ROOT_DIR = os.sep.join(os.path.realpath(__file__).split(os.sep)[:-3])
IMAGE_PATH = os.sep.join([ROOT_DIR, "data", "image"])
JSON_PATH = os.sep.join([ROOT_DIR, "data", "json"])
MAP_PATH = os.sep.join([ROOT_DIR, "data", "map"])
