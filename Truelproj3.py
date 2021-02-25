from Truelproj import Player
import itertools
import random
import functools
import time
import sys
import logging

logging.basicConfig(level=logging.WARNING)


class PvP():
	game_modes = [
	"simultaneous",
	"sequential"
	]

	def __init__(self,players_set=list(),arena_name="Maelstorm Abyss Fight Grounds"):
			 self.arena_name = arena_name.strip()
			 self.all_players = players_set
			 self.alive_players = self.all_players.copy() 
			 self.alive_iter = itertools.cycle(self.all_players)
			 self.targets = dict()
			 
	def opponents_of(self,player):
		return list(set(self.all_players)-{player})
	
	def resurrect_all(self):
		for player in self.all_players: player.resurrect()
		
	#########################################################
	###PVP PROTOCOLS
	def use_random_protocol(self,**kwargs):
			for player in self.alive_players:
				  self.targets[player] = random.choice(
					self.opponents_of(player))
			###SHOW TARGETS/PROTOCOL
			if list(kwargs.values())[0] ==True:
				print("\nPvP Protocol:")
				for player in self.alive_players:
						print("{} ------> {}".format(player.name,self.targets[player].name))
				print()



	def SO_protocol(self):
		pass #TODO


	def duel_protocol(self):
		"""1vs.1 PvP arena protocol"""
		if len(self.all_players)==2:
			self.targets[self.all_players[0]] = self.all_players[1]
			self.targets[self.all_players[1]] = self.all_players[0]
		else:
			raise ValueError

	###########################################################
	###CHECKING WINNING CONDITIONS
	def who_are_alive(self):
		return [bool(player.is_alive()) for player in self.alive_players]



	def remaining_players(self,method="1"):
		assert method.strip()=="1"
		if method.strip() == "1":
			for player in self.alive_players:
				if not player.is_alive():
					self.alive_players.remove(player)
					self.use_random_protocol(show=True)
		elif method.strip() =="2":
			self.alive_players = itertools.compress(self.alive_players,self.who_are_alive())
			self.use_random_protocol(show=True)
		else:
			raise NotImplementedError("You've reached an under construction area... Head back!")


	def terminate_procedure(self,mode="sequential"):
			 if mode.strip() == "sequential":
						print(len(self.alive_players))
						return False if len(self.alive_players)>1 else True
			 elif mode.strip() == "simultaneous":
				 return True if (len(self.alive_players)==0 or len(self.alive_players)==1) else False  
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
				  for player in winners: victorious += "{}\n".format(player.name)
				  print("Last players standing: \n {}.".format(victorious))
			return winners


	def show_health(self,num_rounds):
		for player in self.all_players:
			if player.is_alive():
				print("{:d}: \t {}: \t\t {:1.2f} health.".format(
					num_rounds,player.name,player.hp),end="\n")
			else:
				print("{:d}: \t {}: \t\t Status: Deceased.".format(
					num_rounds,player.name,player.hp),end="\n")

	@staticmethod
	def something_went_wrong(num,loop_tolerance=300):
		if num>loop_tolerance: 
			logging.warning("Infinite loop detected.")
			time.sleep(4)
			sys.exit("Terminating program...") 


	##########################################################
	###INITIALIZE ARENA: MAIN METHOD

	def initialize_arena(self,duel=False,mode="sequential"):
		###CHOOSE PVP Protocol
		if duel:
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

		###Sequential Firing Mode
		if mode.strip() =="sequential":
			while True:
					tik = time.perf_counter()
					self.alive_players[num_rounds%len(self.alive_players)].attack(
						self.targets[self.alive_players[num_rounds%len(self.alive_players)]])
					self.remaining_players()
					num_rounds += 1
					self.show_health(num_rounds)
					if self.terminate_procedure(mode.strip()):
						tak = time.perf_counter()
						print("Game has been completed in {:d} rounds (=total number of shots fired)\n in {:1.2f} seconds.".format(
							num_rounds,float(tak-tik)))
						print("Terminating procedure...")
						break
					PvP.something_went_wrong(num_rounds)
			self.show_winners()
			print("Winner: \t {}".format(self.alive_players[0].name))


		###Simultaneous Firing Mode
		elif mode.strip() == "simultaneous":
			while True:
				tik = time.perf_counter()
				self.alive_players[num_rounds%len(self.alive_players)].attack(
					self.targets[self.alive_players[num_rounds%len(self.alive_players)]])
				num_rounds += 1
				self.show_health(num_rounds)
				if num_rounds%len(self.alive_players)==0:
						 self.remaining_players()
						 if self.terminate_procedure(mode.strip()):
							   tak = time.perf_counter()
							   print("Game has been completed in {:d} rounds (=total number of shots fired)\n in {:1.2f} seconds.".format(
												num_rounds,float(tak-tik)))
							   print("Terminating procedure...")
							   break 
				PvP.something_went_wrong(num_rounds)
				self.show_winners()

		###Not Implemented Game Modes  
		else:
			raise NotImplemented
		input("Press \"Enter\" to terminate process...")
						
			  
	##############################################################
	##OTHER METHODS


	def graph_trees(self):
		pass

	def __repr__(self):
		description = "{}\nActive Players:\n".format(self.arena_name) 
		for player in self.all_players:
			description += "{}\n".format(player.name)
		return description