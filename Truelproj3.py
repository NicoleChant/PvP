from Truelproj import Player
import itertools
import random
import functools
import time
import sys
import logging
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("seaborn")

logging.basicConfig(level=logging.WARNING)


class PvP():
	game_modes = [
	"simultaneous",
	"sequential",
	"RT"
	]

	@staticmethod
	def something_went_wrong(num,loop_tolerance=300):
		if num>loop_tolerance: 
			throw("Infinite loop detected!")


	def __init__(self,players_set=list(),arena_name="Maelstorm Abyss Fight Grounds"):
			 self.arena_name = arena_name.strip()
			 self.all_players = players_set
			 self.alive_players = self.all_players.copy() 
			 self.alive_iter = itertools.cycle(self.all_players)
			 self.targets = dict()
			 self.hp_data = dict()
			 self.dmg_data = dict()
			 for player in self.all_players:
					self.targets.update({player:None})
					self.hp_data.update({player.name:{"Round 0":player.hp}})
					self.dmg_data.update({player.name:{"Round 0":0}})

			 
	def opponents_of(self,player):
		return list(set(self.alive_players)-{player})

	
	def resurrect_all(self):
		for player in self.all_players: player.resurrect()


	def restore_all(self):
		for player in self.all_players: player.restore_to_maxhp()
		print("Players hp were restored...")
		
	#########################################################
	###PVP PROTOCOLS
	def use_random_protocol(self,**kwargs):
			if len(self.alive_players)>1:
				for player in self.alive_players:
						 self.targets[player] = random.choice(
												 self.opponents_of(player))
			###SHOW TARGETS/PROTOCOL
				self.target_descr = "PvP utilised protocols\n"
				if list(kwargs.values())[0] == True:
						 print("\nPvP Protocol:")
						 for player in self.alive_players:
								  self.target_descr += "{:s} ------> {:s}\n".format(
											player.name,self.targets[player].name)
								  print("{:s} ------> {:s}".format(
									  player.name,self.targets[player].name))
						 print()

	def find_opponents_withmaxhp(self,a_player):
		opponents = self.opponents_of(a_player)
		max_val = max([player.hp for player in opponents])
		idx = len(opponents)/2
		while True:
			if opponents[idx].hp==max_val: 
				return opponents[idx]
			elif opponents[idx].hp<max_val: 
				opponents = opponents[(idx+1):]
			else:
				opponents = opponents[:idx]
			idx = len(opponents)/2

	
	def SO_protocol(self):
		if len(self.alive_players)>1:
			for player in self.alive_players:
				self.targets[player] = self.find_opponents_withmaxhp(player)


	def duel_protocol(self):
		"""1vs.1 PvP arena protocol"""
		if len(self.all_players)==2:
			self.targets[self.all_players[0]] = self.all_players[1]
			self.targets[self.all_players[1]] = self.all_players[0]
		else:
			raise ValueError

	###########################################################
	###CHECKING WINNING CONDITIONS
	
	def find_living(self):
		living = dict()
		for player in self.all_players:
			living.update({player:bool(player.is_alive())})
		return living


	def who_are_alive(self):
		return [bool(player.is_alive()) for player in self.alive_players]


	def update_data(self):
		for player in self.all_players:
			self.hp_data[player.name].update(
				{"Round {}".format(len(self.hp_data[player.name])):player.hp})


	def remaining_players(self,method="1"):
		assert method.strip()=="1"
		if method.strip() == "1":
			prev_length = len(self.alive_players)
			for player in self.alive_players:
				if not player.is_alive():
					self.alive_players.remove(player)
			if prev_length!=len(self.alive_players):
				self.use_random_protocol(show=True)
		elif method.strip() =="2":
			self.alive_players = itertools.compress(self.alive_players,self.who_are_alive())
			self.use_random_protocol(show=True)
		else:
			raise NotImplementedError("You've reached an under construction area... Head back!")


	def terminate_procedure(self,mode="sequential"):
			 if mode.strip() == "sequential":
						print(len(self.alive_players))
						return len(self.alive_players)<=1
						#return False if len(self.alive_players)>1 else True
			 elif mode.strip() == "simultaneous":
				 return len(self.alive_players)<=1  
			 else:
				   raise NotImplementedError("You've reached an under construction area... Head back!")


	def show_winners(self):
			winners = [player for player in self.all_players if player.is_alive()]
			if len(winners)==0:
				  print("All players have deceased. It's a DRAW...")
			elif len(winners)==1:
				  print("Last player standing: \t\t {}".format(winners[0].name))
			else:
				  victorious = "\n"
				  for player in winners: 
							  victorious += "{}\n".format(player.name)
				  print("Last players standing: \n {}.".format(victorious))
			return winners


	def show_health(self,num_rounds):
		for player in self.all_players:
			if player.is_alive():
				print("Round {:d}: \t {}: \t\t {:1.2f} health.".format(
					num_rounds,player.name,player.hp),end="\n")
			else:
				print("Round {:d}: \t {}: \t\t Status: Deceased.".format(
					num_rounds,player.name,player.hp),end="\n")



	##########################################################
	###INITIALIZE ARENA: MAIN METHOD

	def initialize_arena(self,mode="sequential"):
		###CHOOSE PVP Protocol
		if len(self.all_players)==2:
				self.duel_protocol()
		else:
				self.use_random_protocol(show=True)

		###SELECT PVP MODE
		#TODO
		

		num_rounds = 0
		num_cycles = 0
		self.show_health(num_rounds)
	
		###INITIALIZE ARENA
		print("Chosen arena mode: \t {:s}".format(mode))
		input("Press \"Enter\" to initialize arena...")
		if mode.strip() not in PvP.game_modes:
				  raise ValueError(
					"The game mode {} is not a valid input.\nPlease use one valid game mode:\nValid Game Modes: \t\t {}".format(
						mode,PvP.game_modes))

		###Sequential Firing Mode
		if mode.strip() =="sequential":
			while True:
					tik = time.perf_counter()
					this_player = self.alive_players[num_rounds%len(self.alive_players)]
					this_player.attack(self.targets[this_player])

					###UPDATING PLAYER HP DATA AFTER *EACH* FIRING ROUND (FIRING MODE=SEQUENTIAL)
					self.update_data()

					###FILTERING DECEASED PLAYERS AFTER *EACH* FIRING ROUND (FIRING MODE=SEQUENTIAL)
					self.remaining_players()

					num_rounds += 1
					self.show_health(num_rounds)


					###CHECKING PROCESS CONDITIONS
					if self.terminate_procedure(mode.strip()):
						break
					PvP.something_went_wrong(num_rounds)
			tak = time.perf_counter()
			print("Game has been completed in {:d} rounds (=total number of shots fired)\n in {:1.2f} seconds.".format(
							num_rounds,float(tak-tik)))
			print("Terminating procedure...")
			self.show_winners()
			print("Winner: \t {}".format(self.alive_players[0].name))


		###Simultaneous Firing Mode
		elif mode.strip() == "simultaneous":
			while True:
				tik = time.perf_counter()
				this_player = self.alive_players[num_rounds%len(self.alive_players)]
				this_player.attack(self.targets[this_player])
				
				num_rounds += 1
				self.show_health(num_rounds)
				if num_rounds%len(self.alive_players)==0:
						 ###UPDATING PLAYER HP DATA AFTER FIRING ROUND (FIRING MODE=SIMULTANEOUS)
						 self.update_data()

						 ###REMOVE DECEASED PLAYERS AFTER FIRING ROUND (FIRING MODE=SIMULTANEOUS)
						 self.remaining_players()

						 ###CHECKING PROCESS CONDITIONS
						 if self.terminate_procedure(mode.strip()):
							   break
				PvP.something_went_wrong(num_rounds)
			tak = time.perf_counter()
			print("Game has been completed in {:d} rounds (=total number of shots fired)\n in {:1.2f} seconds.".format(
												num_rounds,float(tak-tik)))
			print("Terminating procedure...")
			self.show_winners()

		###Not Implemented Game Modes  
		else:
			raise NotImplemented("\"{}\" is not a valid game mode.".format(mode))
		print(self.hp_data)
		print(self.target_descr)
		input("Press \"Enter\" to terminate process...")
						
			  
	##############################################################
	##OTHER METHODS
	def graph_results(self):
		for player in self.all_players:
			xaxis = list(self.hp_data[player.name].keys())
			yaxis = list(self.hp_data[player.name].values())
			plt.plot(
				xaxis,
				yaxis,
				lw=2,
				alpha=1,
				linestyle="--",
				marker="o",
				label="{}".format(player.name)
				)
			plt.xticks(xaxis,rotation=45)
			plt.xlabel("Firing Rounds")
			plt.ylabel("hp")
			the_title = "PvP Results for {:d} players".format(len(self.all_players)) 
			plt.title(the_title)
			plt.legend(loc=0)
		plt.tight_layout()
		plt.show()
						 

	def graph_trees(self):
		pass #TODO

	def __repr__(self):
		description = "{}\nActive Players:\n".format(self.arena_name) 
		for player in self.all_players:
			description += "{}\n".format(player.name)
		return description