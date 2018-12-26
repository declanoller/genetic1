import sys
sys.path.append('../IndividualClasses')
from Population import Population
from Brachistochrone import Brachistochrone
from Skyscraper import Skyscraper


Npop = 25
Npts = 30
height = 1.3
N_gen = 500

# sameness_thresh default 10**-5
# mutate_strength_height_frac default 1/20 , mutate_strength_height_frac=0.2

pop1 = Population(Brachistochrone, Npop, N=Npts, height=height, sameness_thresh=15*10**-2, mutate_strength_height_frac=0.21, same_thresh_decay_steps=N_gen)
ending_state = pop1.plotEvolve(N_gen=N_gen, plot_whole_pop=True, make_gif=True, show_plot=False)

med_88_SS = [[2,3,2,4,4,2,3,1],[1,3,5,3,2,3,2,4],[2,3,2,2,4,6,3,1],[1,2,3,4,3,2,2,4]]

med_88_constlist = [([0,1],1),([1,3],1),([2,1],3),([3,2],3),([4,2],6),([4,3],3),([4,5],5),([5,0],4),([5,4],6),([6,1],2),([6,4],1),([7,4],5)]

med_66_seelist = [[3,2,2,3,1,3],[2,3,1,2,3,3],[3,2,4,4,1,3],[2,4,2,1,3,4]]
med_66_constlist = [([2,1],3),([3,3],2),([3,4],1)]

pop1 = Population(Skyscraper,popsize=10,N=6,see_list=med_66_seelist,const_list=med_66_constlist)
ending_state = pop1.plotEvolve(generations = 7000)


easy_SS = [[2,1,3,2],[2,2,1,3],[2,3,1,3],[3,1,2,2]]






#
