#
#	Authors:	BrianTruong
#					PatricioFigueroa
#
#	Tetris Game Simulator for Learning
#

import sys
import random
import TetrisGame as game

DIGIT = 4
DxG = 4
GENE = DIGIT * DxG + 1
GENES = 23
SMALLEST_DIGIT = 10
POPULATION = 100
CROSSOVER = 0.6
MUTATION = 0.01
GENERATIONS = 10

def processGene(gene):
	#print gene
	positive = bool(int(gene[0], 2))
	
	digits = [(int(gene[(DIGIT*i + 1):(DIGIT*(i+1) + 1)],2) % 10) * SMALLEST_DIGIT / 10.0**i
		for i in xrange(DxG)]
		
	#print digits
	return sum(digits) if positive else -sum(digits)

def chromosomeToWeights(chromosome):
	weights = [processGene(chromosome[i*GENE:(i+1)*GENE])
		for i in xrange(GENES)]
	#print weights
	return weights

def randomInitGene():
	bits = ['0', '1']
	randomGene = [random.choice(bits) for i in xrange(GENES*GENE)]
	return ''.join(randomGene)
	
def sample(pop):
		prob = random.random()
		#print prob
		probSoFar = 0.0
		for ind in pop:
			probSoFar += ind.probability
			#print ind, probSoFar
			if prob < probSoFar:
				return ind

def mutate(chromosome):
	flip = {'0':'1', '1':'0'}
	mutatedChrom = ''
	for i in xrange(len(chromosome)):
		if random.random() < MUTATION:
			mutatedChrom += flip[chromosome[i]]
		else:
			mutatedChrom += chromosome[i]
	#print chromosome
	#print mutatedChrom
	return Individual(mutatedChrom)
	
def crossover(pop, mom):
	#print '==>', pop.chromosome
	#print '==>', mom.chromosome
	childChrom = ''
	for i in xrange(GENES):
		if random.random < CROSSOVER:
			childChrom += pop.chromosome[i*GENE:(i+1)*GENE]
		else:
			childChrom += pop.chromosome[i*GENE:(i+1)*GENE]
	#print '---', childChrom
	return childChrom
				
def nextGeneration(pop):
	nextGen = []
	for i in xrange(POPULATION):
		father = sample(pop)
		mother = sample(pop)
		
		child = mutate(crossover(father, mother))
		nextGen.append(child)
		
	return nextGen
				
class Individual():
	def __init__(self, chromosome):
		self.chromosome = chromosome
		self.fitness = 0
		self.probability = 0.0
		
	def __str__(self):
		return 'Individual < %d , %f >' % (self.fitness, self.probability)

def determineFitness(ind, randSeed):
	baseSeq = [0,1,2,3,4,5,6]*40;
	random.seed(randSeed);
	random.shuffle(baseSeq);
	
	gameLoop = game.Game()
	gameLoop.startGame(0, baseSeq, chromosomeToWeights(ind.chromosome))
	gameLoop.run()
	return gameLoop.gameState.score

def writeFittestWeight(pop, gen):	
	filename = "geneticWeightsGen" + str(gen) + ".tetris"

	fittest = max(pop, key=lambda x: x.fitness)
	weights = chromosomeToWeights(fittest.chromosome)
	
	weightFile = open(filename, 'w')
	for w in weights:
		weightFile.write(str(w) + "\n")
	weightFile.close()

def geneticAlgorithm():
	population = None
	
	for gen in xrange(GENERATIONS):
		print 'Generation %d' % gen
		print '--------------------------------'
		
		# random seed for this generation
		randSeed = random.randint(0,130)
	
		# Spawn or evolve population
		if population is None:
			population = [Individual(randomInitGene()) for i in xrange(POPULATION)]
		else:
			population = nextGeneration(population)
	
		# Determine fitness by simulation
		totalFitness = 0.0
		for individual in population:
			individual.fitness = determineFitness(individual, randSeed)
			totalFitness += individual.fitness
		
		# Normalize fitness
		for individual in population:
			individual.probability = individual.fitness / totalFitness
			#print individual.fitness, '--', individual.probability
			
		writeFittestWeight(population, gen)
		
	for i in population:
		print i
	fittest = max(population, key=lambda x: x.fitness)
	print '==>', fittest
	
	return chromosomeToWeights(fittest.chromosome)
		
def main(argc, argv):
	print "\nTetris Genetic Simulator For Learning"
	print "============================================="

	weights = geneticAlgorithm()
	print weights
	
	'''
	if argc > 1:
		filename = argv[1]
	else:
		filename = "geneticWeights.tetris"
		
	weightFile = open(filename, 'w')
	for w in weights:
		weightFile.write(str(w) + "\n")
	weightFile.close()
	'''
	
if __name__ == "__main__":
	main(len(sys.argv), sys.argv)