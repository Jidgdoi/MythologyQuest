#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# @author Cyril Fournier
# @date 13 Mar 2017

import os,sys

class Item():
	"""
	An item.
	"""
	nextID = 0
	def __init__(self, **kwargs):
		## --- Set default Item attributes
		self.id = self.__generateID__()
		self.name = "Item"
		self.description = "Unset object."
		self.type = "Unset" # Weapon, consumable, armor, crafting ...
		self.stack = None
		self.action = {}
		self.damage = None
		self.armor = None
		self.resistance = {}
		
		## --- Set users attributes
		for k,v in kwargs.items():
			if hasattr(self, k): setattr(self, k, v)
			else: print "\033[1;31mError\033[0m: the attribute {} doesn\'t exist.".format(k)

	def __repr__(self):
		"""
		Representation of the object.
		"""
		txt = "[ %s ] %s\n" %(self.name, self.description)
		if self.type == "consumable":
			txt += " |_ Stack: %s" %(self.stack)
		elif self.type == "weapon":
			txt += " |_ Damage: %s-%s" %(self.damage)
		elif self.type == "cloth":
			txt += " |  Armor: %s\n" %(self.armor)
			txt += " |_ Resistance: {}".format(self.resistance)
		return txt

	def __generateID__(self):
		"""
		Generate ID.
		"""
		Item.nextID += 1
		return "i%d"%Item.nextID

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
