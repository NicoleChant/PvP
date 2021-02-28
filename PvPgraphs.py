####Graphical Representation
import matplotlib.pyplot as plt
from Truelproj import Player
from Truelproj3 import PvP
import numpy as np

plt.style.use("seaborn")

class GraphPvP(PvP):

	def __init__(self,players_set=list(),arena_name="Maelstorm Abyss Fight Grounds"):
		super().__init__(players_set,arena_name)
		#self.colors = colors #TODO

	def graph_results(self):
		for player in self.all_players:
			xaxis = list(self.hp_data[player.name].keys())
			yaxis = list(self.hp_data[player.name].values())
			plt.plot(xaxis,yaxis,
				lw=1,
				alpha=0.6,
				linestyle="--",
				marker="o",
				label="{}".format(player.name))
			plt.xticks(xaxis,rotation=45)
			plt.xlabel("Firing Rounds")
			plt.ylabel("hp")
			plt.title("{}-uel".format(len(self.all_players)))
			plt.legend(loc=0)
		plt.tight_layout()
		plt.show()
						 

