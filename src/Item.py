#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

import os,sys

class Item():
	"""
	An item.
	"""
	def __init__(self, **kwargs):
		self.name = kwargs['name']
		self.description = kwargs['description']
		self.type = kwargs['type'] # Weapon, consumable, armor, crafting ...
		if self.type == "consumable":
			self.stack = kwargs['stack']
			self.action = kwargs['action']
		elif self.type == "weapon":
			self.damage = kwargs['damage']
		elif self.type == "cloth":
			self.armor = kwargs['armor']
			self.resistance = kwargs['resistance']
	
	def __repr__(self):
		"""
		Representation of the object.
		"""
		txt = "%s: %s\n" %(self.name, self.description)
		if self.type == "consumable":
			txt += "   Stack: %d" %(self.stack)
		elif self.type == "weapon":
			txt += "   Damage: %d-%d" %(self.damage)
		elif self.type == "cloth":
			txt += "   Armor: %d\n" %(self.armor)
			txt += "   Resistance: {}".format(self.resistance)
		return txt

## Consumable
HealthPotion = Item(name="Health potion", description="Restore 50pts of health.", type="consumable", stack=1, action={"add":{"health":50}})
ManaPotion   = Item(name="Mana potion", description="Restore 50pts of mana.", type="consumable", stack=1, action={"add":{"mana":50}})

## Weapon
WoodenSword = Item(name="Wooden sword", description="Wooden sword, for children.", type="weapon", damage=(2,3))
WoodenStick = Item(name="Wooden stick", description="Wooden stick, used to lead sheeps.", type="weapon", damage=(1,2))

## Cloth
Cap = Item(name="Cap", description="Small cap made in web.", type="cloth", armor=1, resistance={})
Gloves = Item(name="Gloves", description="Gloves in web.", type="cloth", armor=1, resistance={})


if __name__=='__main__':
	print HealthPotion
	print WoodenSword
	print Cap
