'''
Created on Dec 3, 2014

@author: BrianTruong
'''
import collections
import random
import math
from TetrisModel_MDP import TetrisMDP
from TetrisEvalFuncs import AdvancedEvaluator, AdhocEvaluator
from TetrisGame import GameState
from TetrisAgents import ExpectimaxTetrisAgent, FinitePieceGenerator
import util
import TetrisGame

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
    def __init__(self, actions, discount, featureExtractor, weights, explorationProb=0.1):
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
#         return 0.0001 / math.sqrt(self.numIters)
        return 0.0001

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        curPrediction = self.getQ(state, action)
        actions = self.actions(newState) if newState else []
#         print action
#         for a in actions:
#             print a
#         print len(actions), [self.getQ(newState, a) for a in actions]
        newStateOptValue = max(self.getQ(newState, a) for a in actions) if actions else 0
        residual = (reward + self.discount * newStateOptValue) - curPrediction
#         print 'pred', curPrediction, reward + self.discount * newStateOptValue, residual
        oldQ = 0
        newQ = 0
#         print self.weights
        diff = []
        features = self.featureExtractor(state, action)
        for i, v in enumerate(features):
            oldQ += self.weights[i] * v
            diff.append(self.getStepSize() * residual * v)
            self.weights[i] += self.getStepSize() * residual * v
            newQ += self.weights[i] * v
#         print 'Q', oldQ, newQ, self.getStepSize()
#         print 'diff', diff
#         print 'max', max(features), max(self.weights)
#         print self.weights
            
def simulate(mdp, rl, numTrials=10, maxIterations=100, verbose=False):
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
        for it in xrange(maxIterations):
            if state is None:
                break
            #util.printGrid(state.board.grid)
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
#             print "Trial %d Iter %d (totalReward = %s): %s" % (trial, it, totalReward, sequence)
            print "Trial %d Iter %d (totalReward = %s)" % (trial, it, totalReward)
        totalRewards.append(totalReward)
        if trial % 20 == 0:
            print 'Avg Reward = %f' % (sum(totalRewards[-20:]) / float(len(totalRewards[-20:])))
    return totalRewards

class TetrisGameMDP():
    '''
    A class which encapsulates a Tetris game as an MDP
    '''
    
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
        newGrid, linesCleared, cellsRemoved, landingHeight = action
        reward = linesCleared
        prob = 1.0 / len(oppoActions)
        successors = [nextState.generateSuccessor(1, oppoAction) for oppoAction in oppoActions]
        output = []
        for successor in successors:
            if successor.isWin():
                successor = None
            elif successor.isLose():
#                 reward = -100
                successor = None
            output.append((successor, prob, reward))
        return output
    
    def discount(self):
        return self.tetris.discount()
          
if __name__ == "__main__":
#     weights = TetrisGame.readWeights('weightsThiery.tetris')
    #weights = [0.10000000000000001, 0.5, -44.892192895842715, -88.868713917352991, -9.0845044328524125, 99.48473353935913, -0.10000000000000001, -0.10000000000000001, -46.3552758541178784, -44.894981251780582, -49.903753991739844, -48.776916252514777, -56.009249265806467, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
#     weights = [random.random() for _ in xrange(22)]
    weights = TetrisGame.readWeights('weights_ql400.tetris')
    
#     evaluator = AdvancedEvaluator(weights)
    evaluator = AdhocEvaluator(weights)
    baseSeq = [0,1,2,3,4,5,6]*100
#     random.seed(21)
    random.shuffle(baseSeq);
    
    # state: (board, new piece)
    # action: (newGrid, reward)
    def featureExtractor(state, action):
        newState = state.generateSuccessor(0, action)
        output = evaluator.featureExtractor(newState)
        return output
    
    model = TetrisGameMDP(TetrisMDP(), ExpectimaxTetrisAgent(0, 1, evaluator), FinitePieceGenerator(baseSeq))
    
    qlAlgo = QLearningAlgorithm(model.actions, model.discount(), featureExtractor, weights)
    qlRewards = simulate(model, qlAlgo, numTrials = 100, verbose=True)
    qlAvgReward = float(sum(qlRewards))/len(qlRewards)
    print qlAlgo.weights
    print qlAvgReward
    with open('weights_ql500.tetris', 'w') as f:
        for weight in qlAlgo.weights:
            f.write("{}\n".format(weight))