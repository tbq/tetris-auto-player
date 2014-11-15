'''
Created on Nov 14, 2014

@author: BrianTruong
'''
import tetris
import Pieces
import board
import tetris_algo


class Game:
    
    def __init__(self, seq):
        self.moveHistory = []
        self.gameOver = False
        pieceGenerator = tetris.PieceGenerator(seq)
        self.state = tetris.GameState(board.Board(), pieceGenerator.generateNewPiece(), pieceGenerator)
        self.agents = [tetris_algo.ExpectimaxAgent(), tetris_algo.TetrisPieceAgent()]
    
    def run(self):
        agentIndex = 0
        while not self.state.isLose() and not self.state.isWin():
            # Fetch the next agent
            agent = self.agents[agentIndex]
            action = agent.getAction(self.state)
            if self.state.isLose() or self.state.isWin(): # TODO: due to running out of pieces
                break
            
            # Execute the action
            self.moveHistory.append((agentIndex, action))
            self.state = self.state.generateSuccessor(agentIndex, action)
            agentIndex += 1
            agentIndex = agentIndex % len(self.agents)
            if agentIndex == 0:
                self.state.getLegalActions(agentIndex)
#             print '==================================='
        print 'score = ', self.state.getScore()
        print 'seq index = ', self.state.pieceGenerator.index

if __name__ == '__main__':
#     pieceNames = ['T', 'J', 'S', 'O', 'Z', 'Z', 'I', 'J', 'I', 'I', 'J', 'I', 'I', 'L', 'I', 'O', 'T', 'T', 'J', 'S', 'O', 'T', 'S', 'L', 'I', 'I', 'J', 'L', 'I', 'T', 'T', 'T',
#  'T', 'O', 'O', 'O', 'O', 'S', 'L', 'I', 'T', 'I', 'Z', 'I', 'S', 'J', 'T', 'T', 'L', 'L', 'S', 'L', 'O', 'Z', 'O', 'J', 'J', 'I', 'Z', 'I', 'T', 'I', 'L', 'I',
#  'J', 'I', 'T', 'I', 'L', 'T', 'L', 'S', 'S', 'I', 'Z', 'S', 'Z', 'Z', 'S', 'I', 'Z', 'O', 'O', 'Z', 'T', 'L', 'Z', 'J', 'Z', 'T', 'O', 'O', 'J', 'O', 'J', 'I',
#  'S', 'S', 'S', 'T', 'L', 'O', 'O', 'S', 'L', 'L', 'Z', 'J', 'Z', 'J', 'S', 'T', 'S', 'Z', 'S', 'J', 'O', 'Z', 'Z', 'O', 'O', 'J', 'I', 'L', 'L', 'S', 'O', 'I',
#  'Z', 'L', 'T', 'I', 'S', 'Z', 'O', 'J', 'Z', 'T', 'O', 'S']
#     pieceNames = ['O', 'I', 'O', 'L', 'T', 'L', 'O', 'J', 'L', 'I', 'T', 'O', 'S', 'I', 'I', 'O', 'T', 'S', 'L', 'T', 'Z', 'I', 'J', 'T', 'T', 'I', 'I', 'I', 'I', 'O', 'O', 'T',
#  'S', 'T', 'T', 'Z', 'Z', 'O', 'Z', 'O', 'Z', 'Z', 'O', 'S', 'S', 'L', 'O', 'L', 'I', 'T', 'I', 'T', 'S', 'T', 'I', 'Z', 'Z', 'J', 'T', 'J', 'L', 'I', 'I', 'T',
#  'I', 'L', 'Z', 'Z', 'S', 'O', 'S', 'S', 'L', 'S', 'S', 'S', 'I', 'O', 'Z', 'L', 'S', 'J', 'T', 'Z', 'L', 'J', 'J', 'Z', 'O', 'J', 'J', 'T', 'J', 'O', 'T', 'O',
#  'T', 'J', 'Z', 'J', 'S', 'T', 'L', 'I', 'L', 'S', 'S', 'Z', 'Z', 'J', 'J', 'O', 'L', 'J', 'O', 'L', 'S', 'O', 'L', 'J', 'J', 'Z', 'L', 'I', 'J', 'O', 'L', 'T',
#  'J', 'J', 'S', 'L', 'I', 'L', 'S', 'Z', 'Z', 'S', 'Z', 'I']
    pieceNames = ['I', 'S', 'S', 'J', 'Z', 'T', 'J', 'O', 'O', 'T', 'S', 'J', 'Z', 'T', 'S', 'L', 'I', 'O', 'S', 'J', 'I', 'J', 'I', 'T', 'L', 'O', 'J', 'Z', 'I', 'T', 'J', 'I',
 'T', 'J', 'S', 'T', 'I', 'T', 'J', 'J', 'J', 'L', 'L', 'O', 'J', 'S', 'O', 'O', 'L', 'T', 'Z', 'T', 'Z', 'O', 'T', 'S', 'S', 'T', 'T', 'J', 'L', 'I', 'T', 'L',
 'O', 'J', 'O', 'Z', 'S', 'L', 'I', 'I', 'J', 'Z', 'J', 'J', 'I', 'L', 'O', 'I', 'T', 'J', 'Z', 'L', 'S', 'Z', 'T', 'S', 'O', 'Z', 'L', 'S', 'J', 'L', 'O', 'L',
 'T', 'T', 'Z', 'T', 'Z', 'L', 'J', 'L', 'O', 'Z', 'Z', 'J', 'I', 'T', 'O', 'I', 'S', 'O', 'T', 'Z', 'S', 'T', 'S', 'S', 'I', 'Z', 'I', 'S', 'T', 'Z', 'O', 'I',
 'J', 'O', 'T', 'O', 'J', 'Z', 'O', 'L', 'L', 'S', 'S', 'J']
    seq = [Pieces.pieceByName(pieceName) for pieceName in pieceNames]
#     seq = Pieces.defaultList * 20
    game = Game(seq)
    game.run()
#     for agentIndex, action in game.moveHistory:
#         if agentIndex == 0:
#             board.printGrid(action[0])
#             print 'reward = ', action[1]
#         else:
#             board.printGrid(action.grid)
