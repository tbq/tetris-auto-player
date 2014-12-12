#
#	Authors:	BrianTruong
#					PatricioFigueroa
#
#	Tetris Game Evaluation Functions
#

import util
import random
import TetrisAgents as agents
import TetrisModel_Pieces as pieces
import TetrisModel_Board as board
import TetrisModel_MDP as tetris
import TetrisGame as game

class Evaluator():
	def __init__(self):
		pass
		
	def evaluate(self, gameState):
		pass
		
class BaselineEvaluator(Evaluator):
	def evaluate(self, gameState):
		if gameState.isWin():
			return 1000
		elif gameState.isLose():
			return -100000
		else:
			score = 10*gameState.score -5*gameState.board.findMaxHeight() - 5*gameState.board.findAvgHeight() - 5*gameState.board.countHoles()
			return score		

class AdvancedEvaluator(Evaluator):
	def __init__(self, weights):
		if len(weights) == 0:
			weights = [0]*14
		else:
			print 'Read in weights: ', weights
		self.weights = weights

	def featureExtractor(self, gameState):
		phi = []
		
		# Basic features from state
		phi.append(gameState.score)
		phi.append(gameState.lines)
		
		# Height features
		phi.append(gameState.board.findMaxHeight() / float(gameState.board.rows))
		phi.append(gameState.board.findAvgHeight() / float(gameState.board.rows))
		phi.append(gameState.board.findHeightGap() / float(gameState.board.rows))
		
		# Density features
		phi.append(gameState.board.findDensity())
		
		# Board shape features
		phi.append(gameState.board.getHorizontalRoughness())
		phi.append(gameState.board.getVerticalRoughness())

		#(holes, wells, weightedHoles, highestHole, deepestHole, filled, weightedFilled)
		extraFeats = gameState.board.extraFeatures()
		phi.extend(extraFeats)
				
		return phi
			
	def evaluate(self, gameState):
		if gameState.isWin():
			return 1000
		elif gameState.isLose():
			return -100000
		else:
			feats = self.featureExtractor(gameState)
			weights = self.weights
			
			#print feats
			score = 0
			for i in xrange(len(feats)):
				score += feats[i] * weights[i]
			
			return score
		
		
		
		
		
		
		