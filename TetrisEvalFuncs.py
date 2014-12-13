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
	
	def featureExtractor(self, gameState):
		return []
		
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
		phi.append(0 * gameState.score)
		phi.append(0 * gameState.lines)
		
		# Height features
		nRows = gameState.board.rows
		maxHeight = gameState.board.findMaxHeight()
		avgHeight = gameState.board.findAvgHeight()
		heightGap = gameState.board.findHeightGap()
		phi.append(0 * maxHeight)
		phi.append(0 * avgHeight)
		phi.append(0 * heightGap)
		phi.append(0 * maxHeight / float(nRows))
		phi.append(0 * avgHeight / float(nRows))
		phi.append(0 * heightGap / float(nRows))
		
		# Density features
		phi.append(0 * gameState.board.findDensity())
		
		# Board shape features
		phi.append(0 * gameState.board.getHorizontalRoughness())
		phi.append(0 * gameState.board.getVerticalRoughness())

		#(holes, wells, weightedHoles, highestHole, deepestHole, filled, weightedFilled)
		extraFeats = gameState.board.extraFeatures()
		phi.extend(extraFeats)
		phi.extend((gameState.landingHeight, gameState.getErodedPieceCells(), 
				gameState.board.countRowTransitions(), gameState.board.countColTransitions()))
				
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
		
class AdhocEvaluator(Evaluator):
	def __init__(self, weights):
		self.weights = weights

	def featureExtractor(self, gameState):
		phi = []
		
		phi.extend(gameState.board.border)
		phi.extend(gameState.board.findHeightDiffs())
		phi.append(gameState.board.findMaxHeight())
		#(holes, wells, weightedHoles, highestHole, deepestHole, filled, weightedFilled)
		phi.append(gameState.board.holes)
		phi.append(1)
		return phi		

class DellacherieEvaluator(Evaluator):
	'''
	Inspired by Dellacherie
	'''
	def __init__(self, weights):
		self.weights = weights

	def featureExtractor(self, gameState):
		phi = []

		#(holes, wells, weightedHoles, highestHole, deepestHole, filled, weightedFilled)
		phi.append(gameState.board.holes)
		phi.extend(gameState.board.DellacherieFeatures())
		phi.extend((gameState.landingHeight, gameState.getErodedPieceCells(), 
				gameState.board.countRowTransitions(), gameState.board.countColTransitions()))
		phi.append(1)
		return phi	
		
		
		