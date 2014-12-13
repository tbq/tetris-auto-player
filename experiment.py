'''
Created on Dec 12, 2014

@author: BrianTruong
'''
import random
import numpy as np
import TetrisGame as game

def simulateOneGame(weights):
    baseSeq = [0,1,2,3,4,5,6]*10000;
    random.shuffle(baseSeq);
    
    gameLoop = game.Game()
    gameLoop.startGame(0, baseSeq, weights)
    gameLoop.run()
    return gameLoop.gameState.lines, gameLoop.gameState.score

def simulateGame(weights, N):
    linesV = np.zeros(N)
    scoresV = np.zeros(N)
    for i in xrange(N):
        lines, scores = simulateOneGame(weights)
        linesV[i] = lines
        scoresV[i] = scores
    return linesV, scoresV

def analyze(arr):
    mean = np.mean(arr)
    std = np.std(arr)
    percent5 = np.percentile(arr, 5)
    percent95 = np.percentile(arr, 95)
    print 'mean', mean
    print 'std', std
    print '5%', percent5
    print '95%', percent95
    return mean, std, percent5, percent95

def printArr(arr):
    print '=========='
    for a in arr:
        print a

if __name__ == '__main__':
#     weightFile = 'weights_ql500.tetris'

    results_lines = []
    results_scores = []
    for i in xrange(9,21):
        weightFile = 'weights_ce{}.tetris'.format(i)
        weights = game.readWeights(weightFile)
        linesV, scoresV = simulateGame(weights, 10)
        print '===lines==='
        results_lines.append(analyze(linesV))
        print '===scores==='
        results_scores.append(analyze(scoresV))
    results1 = zip(*results_lines)
    results2 = zip(*results_scores)
    print len(results1), len(results2)
    for result in results1:
        printArr(result)
    for result in results2:
        printArr(result)
    