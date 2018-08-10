
#from Board import Board
#from BoardUnconstrained import BoardUnconstrained
from Population import Population
from Brachistochrone import Brachistochrone

b = Brachistochrone(N=5)
b.getBrachistochroneSol()
b.plotState()

exit(0)

pop1 = Population(Brachistochrone,10,N=30,height=1)

pop1.plotEvolve(generations = 50)




#print(b.fitnessFunction())




'''pop1 = Population(BoardUnconstrained,20,N=30)

pop1.plotEvolve(generations = 2000)

for i in range(5):
    pop1 = Population(BoardUnconstrained,20,N=30)

    pop1.evolve(generations = 500)'''











#
