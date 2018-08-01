# BlackDeath
BlackDeath is a stochastic simulation of disease spread. It simulates the change in a population affected by a disease characterized by three probabilities:
1. Infection probability
2. Death probability
3. Cure probability

Recently, a fourth probability was introduced to add a new dimension to the simulation: vaccination probability. The vaccine probability kicks in after the specified vaccinetime. Once a person is vaccinated, they cannot be infected by the disease again. 

The program displays the simulation time left while running. Also, after execution, it displays three image plots (population stats, initial populace and final populace) and one animation.

Currently, this program can be executed conveniently from Spyder but I will try to make a UI for it soon. 

A notebook version is available to view here (note that this does not contain the vaccination modification):
http://nbviewer.jupyter.org/gist/gauravsdeshmukh/89522824e8838bd2a98a5a9c1a984081
