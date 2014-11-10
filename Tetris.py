'''
Created on Nov 7, 2014

@author: BrianTruong
'''
import collections, random
import board_tools
from Pieces import *
import math
import tetris_algo

# An abstract class representing a Markov Decision Process (MDP).
class MDP:
    # Return the start state.
    def startState(self): raise NotImplementedError("Override me")

    # Return set of actions possible from |state|.
    def actions(self, state): raise NotImplementedError("Override me")

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    # Mapping to notation from class:
    #   state = s, action = a, newState = s', prob = T(s, a, s'), reward = Reward(s, a, s')
    # If IsEnd(state), return the empty list.
    def succAndProbReward(self, state, action): raise NotImplementedError("Override me")

    def discount(self): raise NotImplementedError("Override me")

    # Compute set of states reachable from startState.  Helper function for
    # MDPAlgorithms to know which states to compute values and policies for.
    # This function sets |self.states| to be the set of all states.
    def computeStates(self):
        self.states = set()
        queue = []
        self.states.add(self.startState())
        queue.append(self.startState())
        while len(queue) > 0:
            state = queue.pop()
            for action in self.actions(state):
                for newState, prob, reward in self.succAndProbReward(state, action):
                    if newState not in self.states:
                        self.states.add(newState)
                        queue.append(newState)
        # print "%d states" % len(self.states)
        # print self.states
        
class TetrisMDP(MDP):
    
    def __init__(self):
        pass
    
    def startState(self):
        return (board_tools.Board(), OPiece())
    
    def actions(self, state):
        board, piece = state
        actions = []
        for pieceGrid in piece.getRotations():
            actions.extend(board.tryPlacing(pieceGrid))
        return actions
        
    def succAndProbReward(self, state, action):
        board, piece = state
        newGrid, reward = action
        pieces = [IPiece(), OPiece(), TPiece(), SPiece(), ZPiece(), LPiece(), JPiece()]
        prob = 1.0/len(pieces)
        return [((board(grid = newGrid, linesCompleted = board.linesCompleted + reward), piece), prob, reward) for piece in pieces]
    
    def discount(self):
        return 1
    
if __name__ == "__main__":
    #seq = [OPiece(), SPiece(), ZPiece(), TPiece(), LPiece(), JPiece(), IPiece()] * 2
    model = TetrisMDP()
    qlAlgo = tetris_algo.QLearningAlgorithm(model.actions, model.discount(), tetris_algo.identityFeatureExtractor)
    tetris_algo.simulate(model, qlAlgo)
