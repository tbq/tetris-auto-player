#
#	Authors:	BrianTruong
#					PatricioFigueroa
#
#	Tetris Game Playing Agents
#

import util
import random
import TetrisModel_Pieces as pieces
import TetrisModel_Board as board
import TetrisModel_MDP as tetris
import TetrisEvalFuncs as evalFuncs

from copy import deepcopy

class Agent:
    def __init__(self, index=0):
        self.index = index

    def getAction(self, state):
        raise NotImplementedError("Override me")
		
class PieceGenerator(Agent):
    
	def __init__(self, index, seq = []):
		self.seq = seq
		self.piece = 0;
		Agent.__init__(self, index)
        
	# Get next piece to play
	def getAction(self, state):
		if self.piece < len(self.seq): # get from sequence
			output = self.seq[self.piece]
			self.piece += 1
			return output
		else: # random-generated
			r = random.randint(0, 6)
			return pieces.defaultList[r]
			
class FinitePieceGenerator(Agent):
    
	def __init__(self, index, seq = []):
		self.seq = seq
		self.piece = 0;
		Agent.__init__(self, index)
        
	# Get next piece to play
	def getAction(self, state):
		if self.piece < len(self.seq): # get from sequence
			output = pieces.pieceById(self.seq[self.piece])
			self.piece += 1
			return output
		else: # random-generated
			return None
			
class ExpectimaxTetrisAgent(Agent):
	def __init__(self, index, depth, evaluator):
		self.evaluator = evaluator
		self.depth = depth
		Agent.__init__(self, index)

	def getAction(self, state):

		def computeValue(gameState, index, depth):
			actions =gameState.getActions(index)
			
			if gameState.isGameOver():
				return gameState.getScore()
			elif depth == 0:
				return self.evaluator.evaluate(gameState)
			else:
				values = []
				for action in actions:
					nextState = gameState.generateSuccessor(index, action)
					newIndex = (index + 1) % gameState.getNumAgents()
					newDepth = depth if newIndex != 0 else depth - 1
					value = computeValue(nextState, newIndex, newDepth)
					values.append(value)
				if index == 0:
					return max(values)
				else:
					return sum(values) / float(len(actions))
					
					
		options = []
		actions = state.getActions(self.index)
		if len(actions) == 0:
			return None
			
		for act in actions:
			nextState = state.generateSuccessor(self.index, act)
			nextIndex = (self.index + 1) % state.getNumAgents()
			value = computeValue(nextState, nextIndex, self.depth)
			options.append((value, act))
		
		bestOptions = sorted(options, key=lambda x: x[0], reverse=True)
		maxOptions = [act for val, act in bestOptions if val == bestOptions[0][0]]
		
		#print [val for val, act in options], '\n', [val for val, act in bestOptions], len(maxOptions)
		
		return random.choice(maxOptions);







