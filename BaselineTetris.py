import sys
import random
from copy import deepcopy
from Pieces import *
from board import *

def main():
	print "\nBaseline tetris\n============================\n"
	
	board = Board()
	#print grid.grid
	#print '====='
	#grid.grid[21][0] = 1
	board.printScreen()
	
	for i in range(7):
		oPiece = pieceById(i)
		for p, r, c in oPiece.getRotations():
			print '====', r, "=", c
			oPiece.printGrid(p)		
		print '===========\n==========='
		
	boardChange = [
		[1,0,0,0,0,0,0,0,0,0],
		[1,0,0,0,1,0,1,0,0,0],
		[1,0,0,0,1,1,1,0,0,1],
		[1] * 10,
		[1] * 10
	]
	bcL = len(boardChange)
	
	for row in boardChange:
		for col in row:
			sys.stdout.write(str(col) + " ") 
		sys.stdout.write("\n") 
		
	for i in range(bcL):
		for j in range(10):
			board.grid[i+board.Hlev - bcL - 1][j] = boardChange[i][j]
			
	board.Hlev -= 5
			
	print '===============\n===============\n==============='
	
	board.printScreen()
	#print 'REMOVING ONE LINE'
	#grid.removeLine(grid.grid, 19)
	#grid.printScreen()
	
	#grid.checkForLines(grid.grid)
	#grid.printScreen()
	
	
	print '==============\n==============\n============'
	#pieza = SPiece()
	#piezaRots = pieza.getRotations()
	'''
	for oPiece, r, c in piezaRots:
		test = grid.placePiece((oPiece, r, c), grid.Hlev-r,0)
		grid.checkForLines(test)
		grid.printBoard(test)
		print "La altura es %d" % grid.checkHeight(test)
		print '.'
	'''	
	print '==============\n=========\n=============='
	
	#grid.tryPlacing(piezaRots[0])
	
	return board
	
	
def readSequence(seq):
	screen = Board()
	#screen.printScreen()
	#print '============================'
	pCount = 0
	for p in seq:
		pieza = pieceById(p)
		#print pieza
		bester = (None, float("-inf"))
		for oPiece,  r, c in pieza.getRotations():
			#print '(%dx%d)' % (r,c)
			bester = screen.tryPlacing((oPiece,r,c), bester)
		if bester[0] is None:
			#print "YOU SUCK!!!!!"
			break
		screen.updateBoard(bester)
		#screen.printScreen()
		#print '=================='
		pCount += 1
	return (screen.linesCompleted, pCount)
			
baseSeq = [0,1,2,3,4,5,6]

def simulateTetris(seq, seed):
	print map(pieceNameById, seq)
	
	print 'Sequence Seed:', seed
	lines, pieces = readSequence(seq)
	print "\tTotal Lines Completed:", lines
	print "\tTotal Pieces Handled:", pieces


if __name__ == "__main__":
	seeds = [13, 22, 29]
	mults = [20, 33, 55]
	for i in range(3):
		newSeq = list(baseSeq * mults[i])
		random.seed(seeds[i])
		random.shuffle(newSeq)
		simulateTetris(newSeq[0:140],seeds[i])
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	