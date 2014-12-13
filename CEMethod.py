'''
Created on Dec 12, 2014

@author: BrianTruong
'''
import math
import random
import numpy as np
import TetrisGame as game
from time import gmtime, strftime

def getSampleVector(meanV, sdV):
    d = len(meanV)
    V = np.zeros(d)
    for i in xrange(d):
        V[i] = random.gauss(meanV[i], sdV[i])
    return V

def simulateSeedGame(randSeed, weight):
    baseSeq = [0,1,2,3,4,5,6]*200;
    random.seed(randSeed);
    random.shuffle(baseSeq);
    
    gameLoop = game.Game()
    gameLoop.startGame(0, baseSeq, weight)
    gameLoop.run()
    return gameLoop.gameState.lines

def simulateGame(weight):
    seeds = range(4)
    scores = [simulateSeedGame(seed, weight) for seed in seeds]
    return sum(scores) / len(scores)

def runCrossEntropyIteration(n, k, meanV, sdV):
    d = len(meanV)
    sampleWeightVectors = [getSampleVector(meanV, sdV) for _ in xrange(n)]
    scoreVecs = [(vector, simulateGame(vector)) for vector in sampleWeightVectors]
    scoreVecs.sort(key=lambda x: x[1], reverse=True)
    topScoreVecs = scoreVecs[:k]
    topVectors = [scoreVec[0] for scoreVec in topScoreVecs]
    topScores = [scoreVec[1] for scoreVec in topScoreVecs]
    print 'Average Score', float(sum(topScores)) / len(topScores)
    
    newMeanV = np.zeros(d)
    for vec in topVectors:
        newMeanV += vec
    newMeanV *= 1.0/len(topVectors)
    varianceV = np.zeros(d)
    for vec in topVectors:
        diff = vec - newMeanV
        varianceV += np.square(diff)
    varianceV /= float(len(topVectors))
    newSdV = np.sqrt(varianceV)
    return newMeanV, newSdV

def runCrossEntropyMethod(initMeanV, initSdV):
    n = 30
    rho = 0.1
    k = int(rho * n)
    meanV = initMeanV
    sdV = initSdV
    for i in xrange(11, 101):
        meanV, sdV = runCrossEntropyIteration(n, k, meanV, sdV)
        print strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print i, 'mean', meanV
        print i, 'sd', sdV
        if i % 10 == 0:
            game.writeWeights('weights_ce{}.tetris'.format(i), meanV)
            game.writeWeights('sd_ce{}.tetris'.format(i), sdV)

if __name__ == '__main__':
    initMeanV = np.zeros(8)
    initSdV = np.zeros(8)
    initSdV.fill(10)
#     initMeanV = np.array(game.readWeights('weights_ce10.tetris'))
#     initSdV = np.array(game.readWeights('sd_ce10.tetris'))
    runCrossEntropyMethod(initMeanV, initSdV)