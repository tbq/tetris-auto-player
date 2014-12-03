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
			
		newState = GameState(deepcopy(self.board), deepcopy(self.piece), self.score,
				self.lose, self.win, self.rounds, self.lines)
		
		if agentIndex == 0:
			newGrid, reward = action
			newState.board.updateGrid(newGrid)
			newState.lines += reward
			newState.score += reward*reward
			newState.rounds += 1
		else:
			newState.piece = action
		
		return newState
			
class Game:
    
	def __init__(self):
		pass

	def startGame(self, seq=[], weights=[]):
		self.moveHistory = []
		tetrisGame = tetris.TetrisMDP()
		beginState = tetrisGame.startState()
		self.gameState = GameState(beginState[0], beginState[1], 0, False, False, 0, 0)
		self.agents = [
			#agents.ExpectimaxTetrisAgent(0, 1, evalFuncs.BaselineEvaluator()),
			agents.ExpectimaxTetrisAgent(0, 1, evalFuncs.AdvancedEvaluator(weights)),
			agents.FinitePieceGenerator(1, seq)
		]
	
	def run(self):
		agentIndex = 0
		while not self.gameState.isGameOver():

			agent = self.agents[agentIndex]
			action = agent.getAction(self.gameState)
			print action
			
			self.moveHistory.append((agentIndex, action))
			
			if action is None:
				break
						
			self.gameState = self.gameState.generateSuccessor(agentIndex, action)
			
			agentIndex = (agentIndex + 1) % len(self.agents)
			
		#print self.moveHistory
		#util.printGrid(self.moveHistory[-3][1][0])
		print 'Final score:', self.gameState.score
		print 'Lines completed:', self.gameState.lines
		print 'Pieces played:', self.gameState.rounds
		
def readWeights(filename):
	wF = open(filename)
	w = []
	
	wString = wF.readline()
	while wString:
		w.append(float(wString))
		wString = wF.readline()
		
	return w
	
def main(argc, argv):
	print "Tetris Game Simulation"
	print '============================='
	
	baseSeq = [0,1,2,3,4,5,6]*20;
	#print baseSeq, "\n====\n"
	
	seed(13);
	shuffle(baseSeq);
	
	#print baseSeq
	
	if argc > 1:
		weightFile = argv[1]
	else:
		weightFile = 'weights.tetris'
		
	weights = readWeights(weightFile)
	#print weights
	
	gameLoop = Game()
	gameLoop.startGame(baseSeq, weights)
	gameLoop.run()
	
if __name__ == '__main__':
	main(len(sys.argv), sys.argv)