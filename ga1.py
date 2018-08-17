import sys
sys.path.append('../IndividualClasses')

from Population import Population
from Brachistochrone import Brachistochrone
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve
from Skyscraper import Skyscraper


Npop = 20
Npts = 30
height = .3

b = Brachistochrone(N=Npts,height=height)
b.getBrachistochroneSol()


pop1 = Population(Brachistochrone,Npop,N=Npts,height=height)
ending_state = pop1.plotEvolve(generations = 2000,state_plot_obj=b,plot_whole_pop=True)

exit(0)










easy_SS = [[2,1,3,2],[2,2,1,3],[2,3,1,3],[3,1,2,2]]

med_88_SS = [[2,3,2,4,4,2,3,1],[1,3,5,3,2,3,2,4],[2,3,2,2,4,6,3,1],[1,2,3,4,3,2,2,4]]

med_88_constlist = [([0,1],1),([1,3],1),([2,1],3),([3,2],3),([4,2],6),([4,3],3),([4,5],5),([5,0],4),([5,4],6),([6,1],2),([6,4],1),([7,4],5)]

pop1 = Population(Skyscraper,popsize=10,N=8,see_list=med_88_SS,const_list=med_88_constlist)
ending_state = pop1.plotEvolve(generations = 7000)




sol_x = b.sol[1]
sol_y = b.sol[2]

sol_numeric_y = []

for x_pt in b.xpos:
    f = lambda t: sol_x(t)-x_pt
    tval = fsolve(f,3.14)[0]
    sol_numeric_y.append(sol_y(tval))




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












#
