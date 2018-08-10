
#from Board import Board
#from BoardUnconstrained import BoardUnconstrained
from Population import Population
from Brachistochrone import Brachistochrone

Npop = 20
Npts = 20
height = 1.4

b = Brachistochrone(N=Npts,height=height)
b.getBrachistochroneSol()

pop1 = Population(Brachistochrone,Npop,N=Npts,height=height)
pop1.plotEvolve(generations = 500,state_plot_obj=b)
exit(0)


b.plotState()







#print(b.fitnessFunction())




'''pop1 = Population(BoardUnconstrained,20,N=30)

pop1.plotEvolve(generations = 2000)

for i in range(5):
    pop1 = Population(BoardUnconstrained,20,N=30)

    pop1.evolve(generations = 500)'''











#
