# genetic1

This is code for testing some stuff with Genetic Algorithms (GA).

Population.py is the important class here. It is the one that creates a
population of individuals, controls their mating, mutation, sorts them by fitness
function (FF), and evolves them.

It is designed to be used with any class for the individual, as long as the individual
has these functions:

-fitnessFunction()
-isSameState()
-mate()
-mutate()
-solFound()
-plotState()
-and a .state member variable

I keep my individuals in an IndividualClasses/ directory that's in a different folder
at the same level as this one (so other projects can use the same Individuals),
which is why I add sys.path.append('../IndividualClasses') to the beginning of ga1.py,
but you could just put the individual class in this dir as well.

To create a population, this is how I typically do it:

pop1 = Population(Brachistochrone, Npop, N=20, height=1.3, sameness_thresh=15*10**-2, mutate_strength_height_frac=0.21, same_thresh_decay_steps=N_gen)

-Brachistochrone is the name of the individual class (imported)
-Npop is population size
-Npts, mutate_strength_height, and height are parameters specific to the Brachistochrone class. Population
will check for certain parameters passed to it, but also pass all **kwargs parameters
to the individual class, so parameters that are specific to the class should be passed
to Population's init, like this.

-sameness_thresh and same_thresh_decay_steps are actually also specific to Brachistochrone,
but should probably be incorporated into any problem that's continuous.

Part of what I found, working with this, was that for problems that are continuous like this one,
you need to make sure the solutions can't get too similar to each other while it's searching, or
they will converge to a state that's not even a local minimum, just a little hard to find the way
out of. So that's what sameness_thresh is, it's the threshold below which two states are
considered the same. However, you also want to decrease this as the search gets
finer, so that's what same_thresh_decay_steps is for. It's the number of steps it will
take to geometrically decrease to 10**-5.

This definitely isn't as clear as it could be, so please message me for any questions, comments,
or feedback.
