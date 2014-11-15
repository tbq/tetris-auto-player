'''
Created on Nov 7, 2014

@author: BrianTruong
'''
import collections, random
import board
import Pieces
import math
import tetris_algo
import Pieces
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
        return (board.Board(), Pieces.OPiece())
    
    def actions(self, state):
        board, piece = state
        actions = []
        print board.nPieces
        if board.nPieces < 4:
            for rotatedPiece in piece.getRotations():
                actions.extend(board.tryPlacing(rotatedPiece))
        return actions
        
    def succAndProbReward(self, state, action):
        board = state[0]
        newGrid, reward = action
        pieces = Pieces.defaultList
        prob = 1.0 / len(pieces)
        return [((board.Board(grid=newGrid, linesCompleted=board.linesCompleted + reward,
                                    nPieces=board.nPieces + 1), piece), prob, reward) for piece in pieces]
    
    def discount(self):
        return 1
    
class PieceGenerator:
    
    def __init__(self, seq = []):
        self.seq = seq
        self.index = 0
        
    def generateNewPiece(self):
        if self.index < len(self.seq): # get from sequence
            output = self.seq[self.index]
            self.index += 1
            return output
        else: # random-generated
            r = randint(0, 6)
            return Pieces.defaultList[r]
        
    
class GameState:
    """
    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes.
    
    GameStates are used by the game object to capture the actual state of the game and
    can be used by agents to reason about the game.
    
    Much of the information in a GameState is stored in a GameStateData object.  We
    strongly suggest that you access that data via the accessor methods below rather
    than referring to the GameStateData object directly.
    
    Note that in classic Pacman, Pacman is always agent 0.
    """
    def __init__(self, board, piece, pieceGenerator, score = 0, lost = False):
        self.board = board
        self.piece = piece
        self.pieceGenerator = pieceGenerator
        self.score = score
        self.lost = lost

    ####################################################
    # Accessor methods: use these to access state data #
    ####################################################
    def getLegalActions(self, agentIndex=0):
        """
        Returns the legal actions for the agent specified.
        """
        if self.isWin() or self.isLose(): return []
    
        if agentIndex == 0:
            assignments = []
            for rotatedPiece in self.piece.getRotations():
                assignments.extend(self.board.tryPlacing(rotatedPiece))
            if len(assignments) == 0:
                self.lost = True
            return assignments
        else:
            return Pieces.defaultList

    def generateSuccessor(self, agentIndex, action):
        """
        Returns the successor state after the specified agent takes the action.
        """
        # Check that successors exist
        if self.isWin() or self.isLose(): raise Exception('Can\'t generate a successor of a terminal state.')
    
        # Copy current state
        state = GameState(deepcopy(self.board), deepcopy(self.piece), self.pieceGenerator, self.score)
    
        # Let agent's logic deal with its action's effects on the board
        if agentIndex == 0: # player
            newGrid, reward = action
            state.board.updateGrid(newGrid)
            state.score += reward
        else: # the piece generator
            state.piece = action # the piece generator's action is a piece
        return state
    
    def getNumAgents(self):
        return 2

    def getScore(self):
        return self.score

    def isLose(self):
        return self.lost

    def isWin(self):
        return self.pieceGenerator.index >= len(self.pieceGenerator.seq)  # Never win
    
if __name__ == "__main__":
    # seq = [OPiece(), SPiece(), ZPiece(), TPiece(), LPiece(), JPiece(), IPiece()] * 2
    model = TetrisMDP()
    model.computeStates()
    print len(model.states)
    board1 = board.Board()
    board2 = board.Board()
    print board1 == board2
#     qlAlgo = tetris_algo.QLearningAlgorithm(model.actions, model.discount(), tetris_algo.identityFeatureExtractor)
#     tetris_algo.simulate(model, qlAlgo)
