
#from Board import Board
#from BoardUnconstrained import BoardUnconstrained
from Population import Population
from Brachistochrone import Brachistochrone
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

Npop = 20
Npts = 20
height = .2

b = Brachistochrone(N=Npts,height=height)
b.getBrachistochroneSol()

sol_x = b.sol[1]
sol_y = b.sol[2]

sol_numeric_y = []

for x_pt in b.xpos:
    f = lambda t: sol_x(t)-x_pt
    tval = fsolve(f,3.14)[0]
    sol_numeric_y.append(sol_y(tval))


pop1 = Population(Brachistochrone,Npop,N=Npts,height=height)
ending_state = pop1.plotEvolve(generations = 70,state_plot_obj=b)


diff = np.array(ending_state.state) - np.array(sol_numeric_y)
#print(diff)

temp = Brachistochrone(N=Npts,height=height)

mults = np.linspace(0,1.0,10)
FFs = []
for mult in mults:

    print(mult)
    new_state = sol_numeric_y + diff*mult

    temp.state = new_state

    FFs.append(temp.fitnessFunction())

    plt.plot(temp.xpos,new_state)

print(FFs)
plt.show()



exit(0)

print(ending_state)

ideal_sol = 0



b.plotState()







#print(b.fitnessFunction())




'''pop1 = Population(BoardUnconstrained,20,N=30)

pop1.plotEvolve(generations = 2000)

for i in range(5):
    pop1 = Population(BoardUnconstrained,20,N=30)

    pop1.evolve(generations = 500)'''











#
