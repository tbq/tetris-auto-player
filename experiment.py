'''
Created on Dec 12, 2014

@author: BrianTruong
'''
import random
import numpy as np
import TetrisGame as game

def simulateOneGame(weights):
    baseSeq = [0,1,2,3,4,5,6]*1000;
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
    print 'mean', np.mean(arr)
    print 'std', np.std(arr)
    print '5%', np.percentile(arr, 5)
    print '95%', np.percentile(arr, 95)

if __name__ == '__main__':
    weightFile = 'weights_ql300.tetris'     
    weights = game.readWeights(weightFile)
    linesV, scoresV = simulateGame(weights, 20)
    print '===lines==='
    analyze(linesV)
    print '===scores==='
    analyze(scoresV)