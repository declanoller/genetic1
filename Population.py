import matplotlib.pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors
from time import sleep
from random import randint
from copy import deepcopy
from datetime import datetime
import numpy as np
import os
import FileSystemTools as fst
import subprocess
from math import floor

'''
The object must have the following functions or attributes:
-fitnessFunction()
-mutate()
-isSameState()
-mate()
-state (maybe change to getState()?)
'''

class Population:

    def __init__(self, individ_class, popsize, **kwargs):


        self.kwargs_str = '__'.join(['{}={}'.format(x[0], x[1]) for x in kwargs.items()])
        print(self.kwargs_str)

        self.individ_class = individ_class
        print('using', individ_class.__name__, 'class')
        self.class_name = individ_class.__name__
        self.popsize = popsize
        self.population = [self.createNewIndivid(**kwargs) for i in range(self.popsize)]
        self.sorted_population = None

    def createNewIndivid(self, **kwargs):
        return(self.individ_class(**kwargs))

    def printPop(self):
        print('\nPopulation:')
        [print(individ.state) for individ in self.population]
        print('\n\n')

    def printFitnessFunctions(self):
        for individ in self.population:
            individ.printState()
            print(individ.fitnessFunction())

    def sortIndivids(self):
        individs_fitness = [(individ,individ.fitnessFunction(),'old') for individ in self.population]
        individs_fitness = sorted(individs_fitness,key=lambda x: x[1])
        #print(individs_fitness)
        self.sorted_population = individs_fitness

    def sortTupleByFitness(self,tuple_list):
        return(sorted(tuple_list,key=lambda x: x[1]))

    def getBestAndMean(self):
        if self.sorted_population is None:
            return((0,0))

        best = self.sorted_population[0][1]
        mean = sum([individfitness[1] for individfitness in self.sorted_population])/(1.0*len(self.population))
        return((best,mean))

    def deleteDupes(self,pop):
        #Might have to be careful here -- what happens if you delete so many dupes that the pop size is smaller than original?
        #Pass it just a list of individs. But remember that you have to look at individ.state
        #return(list(set(pop)))

        unique_individs = []
        no_dupes = []
        for i,ind1 in enumerate(pop):
            #if ind1.state not in unique_individs:
            is_not_unique = np.any([ind1.isSameState(other) for other in no_dupes])
            if not is_not_unique:
                unique_individs.append(ind1.state)
                no_dupes.append(ind1)

        return(no_dupes)


    def mateTournament(self):

        best_N = max(int(self.popsize/5), 2)
        self.sortIndivids()
        self.population = [x[0] for x in self.sorted_population]

        new_individs = []
        last_ind = min(len(self.population), self.popsize)
        for i in range(best_N):
            for j in range(i+1,best_N):
                b1,b2 = self.population[i].mate(self.population[j])
                #b1,b2 = self.mate(self.population[i],self.population[j])
                new_individs.append(b1)
                new_individs.append(b2)

        self.population = (new_individs + self.population)[:self.popsize]
        [individ.mutate() for individ in self.population]


    def mateGrid(self):

        new_individs = []

        #Mating scheme
        last_ind = min(len(self.population),self.popsize)
        for i in range(last_ind):
            for j in range(i+1,last_ind):
                b1,b2 = self.population[i].mate(self.population[j])
                #b1,b2 = self.mate(self.population[i],self.population[j])
                new_individs.append(b1)
                new_individs.append(b2)

        '''old_and_new_individs = deepcopy(self.population) + new_individs
        [individ.mutate() for individ in old_and_new_individs]
        self.population = old_and_new_individs + self.population'''

        best_individ = deepcopy(self.population[0])
        self.population = self.population + new_individs
        [individ.mutate() for individ in self.population]
        self.population = self.population + [best_individ]

        self.sortIndivids()

        if len(self.sorted_population) > self.popsize:
            self.population = self.deleteDupes([x[0] for x in self.sorted_population])
        else:
            self.population = [x[0] for x in self.sorted_population]

        self.population = self.population[:self.popsize]




    def plotFF(self, ax, best_FF, mean_FF):

        ax.clear()
        ax.set_xlabel('# generations')
        ax.set_ylabel('fitness function')
        ax.plot(best_FF, label='best', color='dodgerblue')
        ax.plot(mean_FF, label='mean', color='tomato')
        ax.legend()
        ax.text(0.6*len(best_FF), 0.8*max(best_FF), 'best: {:.3f}\nmean: {:.3f}'.format(best_FF[-1], mean_FF[-1]))


    def plotEvolve(self,  **kwargs):

        N_gen = kwargs.get('N_gen', 550)
        show_plot = kwargs.get('show_plot', True)
        plot_state = kwargs.get('plot_state', True)
        plot_whole_pop = kwargs.get('plot_whole_pop', False)
        make_gif = kwargs.get('make_gif', False)
        save_best_FF = kwargs.get('save_best_FF', True)


        date_string = fst.getDateString()
        base_name = f'evolve_{self.class_name}__pop={self.popsize}__gen={N_gen}__{self.kwargs_str}__{date_string}'



        if make_gif:
            N_gif_frames = 100
            gif_dir = fst.combineDirAndFile('gifs', base_name)
            print(gif_dir)
            subprocess.check_call(['mkdir', gif_dir])

        if plot_state:
            fig, axes = plt.subplots(2,1,figsize=(6,8))
            ax_FF = axes[0]
            ax_state = axes[1]
        else:
            fig, ax_FF = plt.subplots(1,1,figsize=(8,8))

        if show_plot:
            plt.show(block=False)

        sol_found = False

        best = []
        mean = []
        cur_best, cur_mean = 0, 0

        method_list = [func for func in dir(self.individ_class) if callable(getattr(self.individ_class, func))]

        if plot_state and plot_whole_pop:
            NUM_COLORS = self.popsize + 2
            cm = plt.get_cmap('RdBu')
            cNorm  = colors.Normalize(vmin=0, vmax=NUM_COLORS-1)
            scalar_map = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
            pop_plot_color_list = [scalar_map.to_rgba(i) for i in range(NUM_COLORS)][::-1]


        for i in range(N_gen):


            self.sortIndivids()
            cur_best, cur_mean = self.getBestAndMean()


            best.append(cur_best)
            mean.append(cur_mean)

            if i%max(1, int(N_gen/20.0))==0:
                print('Generation {}, current best = {:.3f}, current pop. size = {}'.format(i, cur_best, len(self.population)))

            if 'solFound' in method_list:
                if self.population[0].solFound():
                    print(f'found solution in generation {i}!\n')
                    if 'printState' in method_list:
                        self.population[0].printState()
                    break

            # Plot the current best and mean.
            self.plotFF(ax_FF, best, mean)

            # If we're plotting the state of the population, call their plotState() functions.
            # You can plot either the best member, or the whole pop.
            if plot_state:
                ax_state.clear()

                if plot_whole_pop:
                    for j, ind in enumerate(self.population[::-1]):
                        ind.plotState(ax_state, color=pop_plot_color_list[j])

                self.population[0].plotState(ax_state, color='black', plot_sol=True, plot_label=True)

            if show_plot:
                fig.canvas.draw()

            if make_gif:
                if i==0 or (i%max(1, int(N_gen/N_gif_frames))==0):
                    plt.savefig(f'{gif_dir}/{i+1}.png')

            #self.mateTournament()
            self.mateGrid()


        # Finished


        plt.savefig(f'misc_runs/{base_name}.png')

        if save_best_FF:
            np.savetxt(f'misc_runs/bestFF_{base_name}.txt', best)

        if make_gif:
            gif_name = fst.gifFromImages(gif_dir, base_name, ext='.png', delay=10)
            gif_basename = fst.fnameFromFullPath(gif_name)
            subprocess.check_call(['mv', gif_name, fst.combineDirAndFile('misc_runs', gif_basename)])
            subprocess.check_call(['rm', '-rf', gif_dir])

        print('\nending mean = {:.3f}'.format(cur_mean))

        return(self.population[0])


#scrap

'''





'''
