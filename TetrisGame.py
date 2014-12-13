#
#	Authors:	BrianTruong
#					PatricioFigueroa
#
#	Tetris Game Loop
#

import util
import sys
import io
import TetrisModel_Pieces as pieces
import TetrisModel_Board as board
import TetrisModel_MDP as tetris
import TetrisAgents as agents
import TetrisEvalFuncs as evalFuncs

from random import randint, seed, shuffle
from copy import deepcopy
			
class GameState:
	def __init__(self, screen, tetromino, score, lose, win, rounds, lines):
		self.board = screen
		self.piece = tetromino
		self.score = score
		self.lose = lose
		self.win = win
		self.rounds = rounds # total number of plays done = total number of pieces processed by our agent
		self.lines = lines
		self.tetris = tetris.TetrisMDP()
		if self.board.findMaxHeight() >= self.board.rows:
			self.lose = True
		self.linesJustCleared = 0
		self.cellsJustCleared = 0
		self.landingHeight = 0

	def isGameOver(self):
		return self.lose or self.win
		
	def isWin(self):
		return self.win
		
	def isLose(self):
		return self.lose
		
	def getState(self):
		return (self.board, self.piece)
		
	def getScore(self):
		return self.score
		
	def getLines(self):
		return self.lines
		
	def getTotalPiecesProcessed(self):
		return self.rounds
	
	def getErodedPieceCells(self):
		return self.linesJustCleared * self.cellsJustCleared
		
	def getNumAgents(self):
		return 2
		
	def getActions(self, agentIndex):
		if agentIndex == 0:
			actions = self.tetris.actions(self.getState())
			if len(actions) == 0:
				self.lose = True
		else:
			actions = pieces.defaultList
		
		return actions
					
	def generateSuccessor(self, agentIndex, action):
		if self.isGameOver():
			raise Exception('Game is over, no more successors to generate')
			
# 		newState = GameState(deepcopy(self.board), deepcopy(self.piece), self.score,
# 				self.lose, self.win, self.rounds, self.lines)
		newState = deepcopy(self)
		
		if agentIndex == 0:
			newGrid, linesCleared, cellsRemoved, landingHeight = action
			newState.board.updateGrid(newGrid)
			newState.lines += linesCleared
			newState.score += linesCleared*linesCleared
			newState.rounds += 1
			newState.linesJustCleared = linesCleared
			newState.cellsJustCleared = cellsRemoved
			newState.landingHeight = landingHeight
		else:
			newState.piece = action
		
		return newState
			
class Game:
    
	def __init__(self):
		pass

	def startGame(self, depth=1, seq=[], weights=[]):
		self.moveHistory = []
		tetrisGame = tetris.TetrisMDP()
		beginState = tetrisGame.startState()
		self.gameState = GameState(beginState[0], beginState[1], 0, False, False, 0, 0)
		self.agents = [
			#agents.ExpectimaxTetrisAgent(0, 1, evalFuncs.BaselineEvaluator()),
# 			agents.ExpectimaxTetrisAgent(0, depth, evalFuncs.AdhocEvaluator(weights)),
			agents.ExpectimaxTetrisAgent(0, depth, evalFuncs.DellacherieEvaluator(weights)),
			agents.FinitePieceGenerator(1, seq)
		]
	
	def run(self, verbose=False):
		agentIndex = 0
		while not self.gameState.isGameOver():
			if verbose and agentIndex == 0:
				util.printGrid(self.gameState.board.grid)
				print self.agents[0].evaluator.featureExtractor(self.gameState)

			agent = self.agents[agentIndex]
			action = agent.getAction(self.gameState)
			
			if verbose:
				self.moveHistory.append((agentIndex, action))
			
			if action is None:
				break
						
			self.gameState = self.gameState.generateSuccessor(agentIndex, action)
			
			agentIndex = (agentIndex + 1) % len(self.agents)
			
		#print self.moveHistory
		#util.printGrid(self.moveHistory[-3][1][0])
		if verbose:
			print 'Final score:', self.gameState.score
			print 'Lines completed:', self.gameState.lines
			print 'Pieces played:', self.gameState.rounds - 1
		
def readWeights(filename):
	with open(filename, 'r') as f:
		w = []
		for line in f:
			w.append(float(line))
		return w

def writeWeights(filename, weights):
	with open(filename, 'w') as f:
		for weight in weights:
			f.write('{}\n'.format(weight))
	
def main(argc, argv):
	print "Tetris Game Simulation"
	print '============================='
	
	baseSeq = [0,1,2,3,4,5,6]*100;
	#print baseSeq, "\n====\n"
	
	#seed(21);
	#seed(4)
	shuffle(baseSeq);
	
	#print baseSeq
	
	if argc > 1:
		weightFile = argv[1]
	else:
# 		weightFile = 'weights_ql300.tetris'
# 		weightFile = 'geneticWeights.tetris'
# 		weightFile = 'geneticWeightsGen0.tetris'
# 		weightFile = 'geneticWeightsGen1.tetris'
# 		weightFile = 'geneticWeightsGen9.tetris'
# 		weightFile = 'weightsThiery.tetris'
		weightFile = 'weights_ce10.tetris'
		
	weights = readWeights(weightFile)
	#weights = [0.10000000000000001, 0.5, -44.892192895842715, -88.868713917352991, -9.0845044328524125, 99.48473353935913, -0.10000000000000001, -0.10000000000000001, -46.3552758541178784, -44.894981251780582, -49.903753991739844, -48.776916252514777, -56.009249265806467, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	#weights = [0.10000000000000001, 18.692192314534012, -30.559441135215451, -79.790955493495701, -3.0284522805710377, 117.61079877952663, -0.10000000000000001, -0.10000000000000001, -17.936666592822963, -21.197595951521954, -30.934875542030095, -33.86864786051256, -45.78751684601162, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	#weights = [0.10000000000000001, 8.9290518982815605, -27.543567204530063, -74.690538168473211, -4.2843605308798809, 99.484733539359127, -0.10000000000000001, -0.10000000000000001, -24.545680551585356, -24.42373648813615, -31.173483591026667, -33.443551266304716, -39.087170373181067, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	#weights = [0.10000000000000001, 0.5, -20.035879911365605, -66.0879108327198, -5.6233288221681255, 99.484733539359127, -0.10000000000000001, -0.10000000000000001, -26.993167882850717, -24.346022953567569, -27.787043799824712, -22.509037540754889, -27.041543811219753, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	#weights = [0.10000000000000001, 0.5, -44.892192895842712, -88.868713917352991, -9.0845044328524125, 110.40108328734912, -0.10000000000000001, -0.10000000000000001, -31.88725515464564, -31.997002607579162, -37.281055312507362, -36.427017385752833, -44.934307987291923, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	#print weights
	
	gameLoop = Game()
	gameLoop.startGame(1, baseSeq, weights)
	gameLoop.run(True)
	
if __name__ == '__main__':
	main(len(sys.argv), sys.argv)