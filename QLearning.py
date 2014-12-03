'''
Created on Dec 3, 2014

@author: BrianTruong
'''
import collections
import random
import math
from TetrisModel_MDP import TetrisMDP
from TetrisEvalFuncs import AdvancedEvaluator
from TetrisGame import GameState
from TetrisAgents import ExpectimaxTetrisAgent, FinitePieceGenerator
import util

class RLAlgorithm:
    # Your algorithm will be asked to produce an action given a state.
    def getAction(self, state): raise NotImplementedError("Override me")

    # We will call this function when simulating an MDP, and you should update
    # parameters.
    # If |state| is a terminal state, this function will be called with (s, a,
    # 0, None). When this function is called, it indicates that taking action
    # |action| in state |state| resulted in reward |reward| and a transition to state
    # |newState|.
    def incorporateFeedback(self, state, action, reward, newState): raise NotImplementedError("Override me")

class QLearningAlgorithm(RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, weights, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = weights
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for i, v in enumerate(self.featureExtractor(state, action)):
            score += self.weights[i] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        actions = self.actions(state)
        if actions:
            if random.random() < self.explorationProb:
                return random.choice(self.actions(state))
            else:
                return max(((self.getQ(state, action), action) for action in self.actions(state)), key=lambda x: x[0])[1]
        else:
            return None

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        curPrediction = self.getQ(state, action)
        actions = self.actions(newState)
        newStateOptValue = max(self.getQ(newState, a) for a in actions) if actions else 0
        residual = (reward + self.discount * newStateOptValue) - curPrediction
        for i, v in enumerate(self.featureExtractor(state, action)):
            self.weights[i] += self.getStepSize() * residual * v
            
def simulate(mdp, rl, numTrials=10, maxIterations=1000, verbose=False):
    # Return i in [0, ..., len(probs)-1] with probability probs[i].
    def sample(probs):
        target = random.random()
        accum = 0
        for i, prob in enumerate(probs):
            accum += prob
            if accum >= target: return i
        raise Exception("Invalid probs: %s" % probs)

    totalRewards = []  # The rewards we get on each trial
    for trial in range(numTrials):
        state = mdp.startState()
        sequence = [state]
        totalDiscount = 1
        totalReward = 0
        for _ in range(maxIterations):
            util.printGrid(state.board.grid)
            action = rl.getAction(state)
            if action is None:
                break
            transitions = mdp.succAndProbReward(state, action)
            if len(transitions) == 0:
                rl.incorporateFeedback(state, action, 0, None)
                break

            # Choose a random transition
            i = sample([prob for newState, prob, reward in transitions])
            newState, prob, reward = transitions[i]
            sequence.append(action)
            sequence.append(reward)
            sequence.append(newState)

            rl.incorporateFeedback(state, action, reward, newState)
            totalReward += totalDiscount * reward
            totalDiscount *= mdp.discount()
            state = newState
        if verbose:
            print "Trial %d (totalReward = %s): %s" % (trial, totalReward, sequence)
        totalRewards.append(totalReward)
    return totalRewards

class TetrisGameMDP():
    
    def __init__(self, tetris, player, opponent):
        self.tetris = tetris
        self.player = player
        self.opponent = opponent
    
    def startState(self):
        tetrisStartState = self.tetris.startState()
        return GameState(tetrisStartState[0], tetrisStartState[1], 0, False, False, 0, 0)
    
    def actions(self, state):
        return state.getActions(0)
        
    def succAndProbReward(self, state, action):
        nextState = state.generateSuccessor(0, action)
        oppoActions = state.getActions(1)
        newGrid, reward = action
        prob = 1.0 / len(oppoActions)
        successors = [nextState.generateSuccessor(1, oppoAction) for oppoAction in oppoActions]
        output = []
        for successor in successors:
            if successor.isWin() or successor.isLose():
                successor = None
            output.append((successor, prob, reward))
        return output
    
    def discount(self):
        return 1
          
if __name__ == "__main__":
    evaluator = AdvancedEvaluator([])
    baseSeq = [0,1,2,3,4,5,6]*20
    
    # state: (board, new piece)
    # action: (newGrid, reward)
    def featureExtractor(state, action):
        newState = state.generateSuccessor(0, action)
        output = evaluator.featureExtractor(newState)
        return output
    
    model = TetrisGameMDP(TetrisMDP(), ExpectimaxTetrisAgent(0, 1, evaluator), FinitePieceGenerator(baseSeq))
    weights = [1, 5, -1, -1, -1, -1, -1, -10, 0, 0, 0, 0, 0, 0]
    qlAlgo = QLearningAlgorithm(model.actions, model.discount(), featureExtractor, [0] * 14)
    qlRewards = simulate(model, qlAlgo, numTrials = 10)
    qlAvgReward = float(sum(qlRewards))/len(qlRewards)
    print qlAlgo.weights
    print qlAvgReward