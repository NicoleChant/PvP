#Truels Project
import random
import itertools
import functools
import time

def cooldown(func_method):
	@functools.wraps(func_method)
	def waiting_time(self,*args):
		tik = time.perf_counter()
		func_method(*args)
		tak = time.perf_counter()
	return waiting_time

class Player():
	available_kwargs = [
	"armor",
	"arpen",
	"hp",
	"effective_hp",
	"critical_chance",
	"critical_strike_dmg",
	"evade_chance",
	"base_dmg",
	"attack_speed",
	"multiple_strike_chance",
	"num_of_multiple_strikes",
	"DPS",
	"mana",
	"mana_regen_unit",
	"casting_speed",
	"spell_power",
	"hp_regen",
	"hp_regen_unit",
	"gold",
	"inventory",
	"max_inventory"
	]

	default_attrs = {
	   "armor":0,
	   "arpen":0,
	   "hp":20,
	   "critical_chance":0,
	   "critical_strike_dmg":0,
	   "evade_chance":0,
	   "mana":0,
	   "mana_regen":0,
	   "multiple_strike_chance":0,
	   "num_of_multiple_strikes":2,
	   "casting_speed":0,
	   "spell_power":0,
	   "base_dmg":5,
	   "alive":True,
	   "attack_speed":1,
	   "hp_regen":0,
	   "hp_regen_unit":1,
	   "gold":500,
	   "inventory":list(),
	   "max_inventory":6
	}

	time_unit = "sec"

	def __init__(self,name="Alice"):
			self.name = name.strip()
			for key, value in Player.default_attrs.items():
						  setattr(self,key,value)
			self.effective_health = self.effective_hp()
			#self.alive = True #default value
			self.max_hp = self.hp #initial hp cap
			self.resper = 1.0 #resurrection max_hp%

			#self.init_regen()
			#TODO TO BE IMPLEMENTED (Parallel processing)

	##############################################################
	#GENERAL PLAYER METHODS
	@staticmethod
	def is_float(value):
		try:
			float(value)
			return True
		except: return False

	def rename(self,name):
		oldname = self.name 
		self.name = name
		print("Player {} has been succesfully renamed to {}".format(
			oldname,self.name))

	def update_properties(self,**kwargs):
		for key , value in kwargs.items():
			if key in Player.available_kwargs:
				if key!=str(name): self.__dict__[key] += value
		print("Player {} properties have been succesfully updated!".format(
			{self.name}))


	###################################################################
	#INVENTORY METHODS
	@property
	def inventory_size(self):
			return len(self.inventory)

	def pick_item(self,item):
		if self.inventory_size<self.max_inventory:
			self.inventory.append(item)
			try:
				for key in item:
					if key!=str(name): self.__dict__[key] += item[key]
				print("The heroine seems now stronger than ever...!")
			except:
				print("Not a dictionary...")
			print("Item {} was added to your inventory.".format(item))
		else:
			print("Your inventory is full!")

	def drop_item(self,item):
		if item in self.inventory:
			self.inventory.remove(item)
			print("Item {} was dropped from your inventory.".format(item))
		else:
			print("Item {} cannot be found in your inventory.".format(item))

	def show_inventory(self):
		attr = "inventory"
		if attr in self.__dict__.keys():
			print("Players inventory: ",end="\n")
			for item in self.inventory:
					 print("{}".format(item),end="\n")
			print()
		else: print("No such attribute {}.".format(attr))


	##########################################################
	###PvP MECHANICS METHODS

	def resurrect(self):
		if self.alive:
			print("Player {:s} is alive. You cannot resurrect an alive player.".format(self.name))
		else:
			self.hp = self.max_hp*(1-self.resper)
			print("Player {:s} has been resurrected with {:1.2f}/% total hp (={:1.2f} hp).".format(
				self.name,100*self.hp/self.max_hp,self.hp))

	def restore_to_maxhp(self):
		self.hp = self.max_hp

	def is_alive(self):
		self.alive = self.hp>0
		return self.alive

	@property
	def normal_dmg(self,mu,var):
		return self.base_dmg + random.gauss(mu,var)

	@staticmethod
	def armor_func(armor,k=1,constant=100):
		return armor**k/(armor**k+constant) if armor>=0 else (1-armor**k)/(armor**k+constant)

	@staticmethod
	def arpen_func(arpen,k=1,constant=100):
		return arpen**k/(arpen**k+constant) if arpen>=0 else 0

	def effective_hp(self,on_arpen=0):
		  return self.hp/(1-Player.armor_func(self.armor*
			(1-Player.arpen_func(on_arpen)
				)
			)
		  ) if self.hp>=0 else 0

	def reduced_dmg(self,on_armor=0):
		return self.base_dmg*(1-Player.armor_func(on_armor*
			(1-Player.arpen_func(self.arpen)
				)
			)
		  ) if self.base_dmg>=0 else 0


	def init_regen(self):
			self.hp += self.hp_regen
			self.mana += self.mana_regen

	def evaded_strike(self):
		return 1 if random.random()<=self.evade_chance else 0

	def critical_strike(self):
		return 1 if random.random()<=self.critical_chance else 0

	def multiple_strike(self):
		return 1 if random.random()<=self.multiple_strike_chance else 0

	def apply_multiple_strikes(self,induced_dmg):
		return induced_dmg*self.num_of_multiple_strikes

	def apply_dmg(self,on_armor=0,true_dmg=False):
		crit_strik = self.critical_strike()
		multiple_strik = self.multiple_strike()
		if crit_strik == 1: print("CRITICAL STRIKE!")
		if multiple_strik == 1: print("{} MULTIPLE STRIKES".format(self.num_of_multiple_strikes))
		if not true_dmg:
			return self.reduced_dmg(on_armor)*(
			1+crit_strik*self.critical_strike_dmg) if multiple_strik==0 else self.reduced_dmg(on_armor)*(
			1+crit_strik*self.critical_strike_dmg)*self.num_of_multiple_strikes
		else:
			return self.base_dmg*(
			1+crit_strik*self.critical_strike_dmg) if multiple_strik==0 else self.reduced_dmg(on_armor)*(
			1+crit_strik*self.critical_strike_dmg)*self.num_of_multiple_strikes

	def attack(self,other,true_dmg=False):
		if isinstance(other,Player):
				induced_dmg = self.apply_dmg(other.armor,true_dmg)*(1-other.evaded_strike())
				other.hp -= induced_dmg
				print(induced_dmg)
				return induced_dmg
		else:
			   print("The target is a non-{} object...".format(Player.__name__)) 

	
	##########################################################
	#STRING OUTPUT METHODS

	def __repr__(self):
		sep = "-"*50+"\n"
		description = sep+"Player {}\n".format(self.name)
		description += sep+"Player attributes & statistics:\n"+"*"*50+"\n"
		longest_key = max([len(attr) for attr in Player.available_kwargs])

		#showing attributes
		for key, value in self.__dict__.items():
				if key!="inventory" and key!="name":
					description += "{:s}:".format(
						key) + " "*(longest_key-len(key)
						)+"\t\t\t {:1.2f}\n".format(
						value) + sep

		#showing items
		description += "Possessed items: "
		if len(self.__dict__["inventory"])>0:
			description += "\n"
			for item in self.__dict__["inventory"]:
				 description += "{}\n".format(item) 
		else: description += "\t\t\t None\n" + sep
		return description+"\n"