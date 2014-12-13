#
#	Authors:	BrianTruong
#					PatricioFigueroa
#
#	Tetris Model: Board (Screen)
#

import collections, random
import math
#import tetris_algo
import TetrisModel_Pieces as pieces
import TetrisModel_Board as board
from copy import deepcopy
from random import randint

# An abstract class representing a Markov Decision Process (MDP).
class MDP:
    # Return the start state.
    def startState(self): raise NotImplementedError("Override me")

    # Return set of actions possible from |state|.
    def actions(self, state): raise NotImplementedError("Override me")

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    def succAndProbReward(self, state, action): raise NotImplementedError("Override me")

    def discount(self): raise NotImplementedError("Override me")

    
class TetrisMDP(MDP):
    
    def __init__(self):
        pass
    
    def startState(self):
        return (board.Board(), pieces.OPiece())
    
    def actions(self, state):
        screen, piece = state
        actions = []
        #print screen.nPieces
        if screen.nPieces < 4:
            for rotatedPiece in piece.getRotations():
                actions.extend(screen.tryPlacing(rotatedPiece))
        return actions
        
    def succAndProbReward(self, state, action):
        screen = state[0]
        newGrid, reward = action
        prob = 1.0 / len(pieces.defaultList)
        return [((board.Board(grid=newGrid, linesCompleted=screen.linesCompleted + reward,
                                    nPieces=screen.nPieces + 1), piece), prob, reward) for piece in pieces.defaultList]
    
    def discount(self):
        return 1
#         return 0.6
    
if __name__ == "__main__":
	model = TetrisMDP()
	begin = model.startState()
	print begin
	beginActions = model.actions(begin)
	print beginActions
	print model.succAndProbReward(begin, beginActions[0])
	print '\nEq test:'
	board1 = board.Board()
	board2 = board.Board()
	print board1 == board2
#     qlAlgo = tetris_algo.QLearningAlgorithm(model.actions, model.discount(), tetris_algo.identityFeatureExtractor)
#     tetris_algo.simulate(model, qlAlgo)
