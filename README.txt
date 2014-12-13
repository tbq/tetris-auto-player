CS221 Final Project README

Ba Quan Truong
Sergio Patricio Figueroa Sanz
Narek Tovmasyan

Automatic Tetris Player

==============================================

The following is a list of flles found in this project and what their contents are:

TetrisGame.py -> Main Tetris game play loop. This file contains a Game class and a GameState class that run the complete game. Calling this file as:
		python TetrisGame.py
will initiate a run of Tetris.
Additionally, providing as a parameter a path to a file with weights to the program will cause it to use those weights (rather than default zero vector) when evaluating states. This is useful to test the learned weights from our algorithms:
		python TetrisGame.py <weights file>
When executed, it also prints the board at each step.
		
TetrisAgents.py -> File containing a series of Game Agents that play the game of Tetris. Specifically, there are two "players" for how tetrominoes are generated (finite and infinite), and two agents that actually play the game (one based on the baseline / hand-tuned evaluation function and another that uses the many features we incoirporated into our model)

TetrisEvalFuncs.py -> Actually contains implementations of the evaluation functions used by the Agents from the previous file.

TetrisModel_Board.py -> MDP implementation of Tetris, contains method related to the board, placing of pieces on the board etc.

TetrisModel_MDP.py -> MDP implementation of Tetris, actual MDP that is at the center of the model for Tetris

TetrisModel_Pieces.py -> MDP implementation of Tetris, contains a Piece class and extensions for all seven tetrominoes and a few helper functions;

QLearning.py -> Implementation of the Q-Learning algorithm for use in determining optimal weights for our Tetris evaluation function.

CEMethod.py -> Implementation of the Cross-Entropy method to determine optimal weights

TetrisSimulator.py -> Contains the genetic algorithm to find the optimal set of weight for our Tetris playing agents. When called, can take an argument for the type of fitness evaluation the learner uses (score or lines):
		python TetrisSimulator.py [ -score | -lines ]

util.py -> Couple of helper functions

experiment.py -> Used to measure the performance of computed weight vectors