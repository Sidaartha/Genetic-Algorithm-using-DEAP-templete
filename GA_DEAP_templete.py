#---------------------------------------------- Importing Libraries -------------------------------------------

import random
from deap import algorithms, base, tools, creator

#------------------------------------------------- Variable info ----------------------------------------------

n 	= 			# No.of individuals in each population
m	=   		# No.of gen in an individual 
n_i = 		 	# Lower limit of gen in an individual
n_f	= 		 	# Upper limit of gen in an individual
NGen 	= 			# Number of generations/Number of itterations			
CXPB	= 0.5		# CXPB  is the probability with which two individuals are crossed
MUTPB 	= 0.2		# MUTPB is the probability for mutating an individual

#----------------------------------------------- Fitness Function ----------------------------------------------

def FitnessFunc(individual):

	''' <CODE> '''

	return fitness_value, 

# ------------------------------------------------ Creating class -----------------------------------------------

# Weights to maximise(i.e, +ve) or minimise(i.e, -ve) the fitness function.
# Can add multiple wts for multi objective functions,
# But it will check the 2nd objective if there are multiple individuals with same fitness values for 1st objective.
creator.create('Fitness', base.Fitness, weights = (1.0, ))
creator.create('Individual', list, fitness = creator.Fitness)

toolbox = base.Toolbox()
toolbox.register('attr_value', random.randint, n_i, n_f)	# generator
# Structure initializers
toolbox.register('individual', tools.initRepeat, creator.Individual, toolbox.attr_value, m)	
toolbox.register('population', tools.initRepeat, list, toolbox.individual)
# genetic operators required for the evolution
toolbox.register('evaluate', FitnessFunc)
toolbox.register('mate', tools.cxTwoPoint)
toolbox.register('mutate', tools.mutUniformInt, low=n_i, up=n_f, indpb=0.2)
toolbox.register('select', tools.selTournament, tournsize=3)

#=========================================== Evolution operation ================================================
#-------------------------------------------( Genetic Algorithm )------------------------------------------------

def Evolution(n, CXPB, MUTPB, NGen):

	# create an initial population of 'n' individuals
	pop = toolbox.population(n)

	print("Start of evolution")
	
	# Evaluate the entire population
	fitnesses = list(map(toolbox.evaluate, pop))
	for ind, fit in zip(pop, fitnesses):
		ind.fitness.values = fit
	
	print("  Evaluated %i individuals" % len(pop))

	# Extracting all the fitnesses of 
	fits = [ind.fitness.values[0] for ind in pop]

	# Begin the evolution
	for g in range(NGen):

		gen = g+1
		print("-- Generation %i --" % gen)
		
		# Select the next generation individuals
		offspring = toolbox.select(pop, len(pop))
		# Clone the selected individuals
		offspring = list(map(toolbox.clone, offspring))
	
		# Apply crossover and mutation on the offspring
		for child1, child2 in zip(offspring[::2], offspring[1::2]):

			# cross two individuals with probability CXPB
			if random.random() < CXPB:
				toolbox.mate(child1, child2)
				# fitness values of the children
				# must be recalculated later
				del child1.fitness.values
				del child2.fitness.values

		for mutant in offspring:
			# mutate an individual with probability MUTPB
			if random.random() < MUTPB:
				toolbox.mutate(mutant)
				del mutant.fitness.values
	
		# Evaluate the individuals with an invalid fitness
		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		fitnesses = map(toolbox.evaluate, invalid_ind)
		for ind, fit in zip(invalid_ind, fitnesses):
			ind.fitness.values = fit
		print("  Evaluated %i individuals" % len(invalid_ind))
		
		# The population is entirely replaced by the offspring
		pop[:] = offspring
		
		# Gather all the fitnesses in one list and print the stats
		fits = [ind.fitness.values[0] for ind in pop]
		
		length = len(pop)
		mean = sum(fits) / length
		sum2 = sum(x*x for x in fits)
		std = abs(sum2 / length - mean**2)**0.5

		print("  Min %s" % min(fits))
		print("  Max %s" % max(fits))
		print("  Avg %s" % mean)
		print("  Std %s" % std, '\n')
	
	print("-- End of successful evolution --")

	Best = tools.selBest(pop, 1)[0]	
	print("Best individual is %s, %s" % (Best, Best.fitness.values))

	return Best

# ======================================== Running Genetic Algorithm =========================================

Best_ind = Evolution(n, CXPB, MUTPB, NGen)

# ------------------------------------------------------------------------------------------------------------