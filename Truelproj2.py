from Truelproj import Player
from Truelproj3 import PvP
import sys
import logging

logging.basicConfig(level=logging.WARNING)

class Main():
	a_player = Player("Nicole")
	print(a_player)
	a_player2 = Player("Alice")
	a_player3 = Player("Bob")
	a_player4 = Player("Donald Duck")
	
	# print(a_player2.hp)
	# print(a_player.attack(a_player2))
	# print(a_player2.hp)
	players = [a_player,a_player2,a_player3,a_player4]
	an_arena = PvP(players)
	print(an_arena)
	an_arena.initialize_arena("sequential")
	an_arena.graph_results()



if __name__=="__main__": Main()