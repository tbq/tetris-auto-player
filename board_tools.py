import sys
import numpy as np
from copy import deepcopy
from Pieces import *

def findBorder(a, isTop = True):
	border = np.empty((a.shape[1]), np.int8)
	border.fill(-1)
	for c in xrange(a.shape[1]):
		# search from top if isTop and from bottom otherwise
		searchedRange = reversed(xrange(a.shape[0])) if isTop else xrange(a.shape[0])
		for r in searchedRange:
			if a[r,c] != 0:
				border[c] = r
				break
	return border

def tryRemoveLines(grid, start, end):
	sums = np.sum(grid[start:end, : ], axis = 1)
	fullLines = [start + i for i in xrange(sums.shape[0]) if sums[i] == grid.shape[1]]
	if fullLines:
		removeLines(grid, fullLines)
	return len(fullLines)
	
def removeLines(grid, fullLines):
	visited = 0
	for r in xrange(fullLines[0], grid.shape[0]):
		if visited < len(fullLines) and r == fullLines[visited]:
			visited += 1
		else:
			grid[r-visited,:] = grid[r,:]
	for r in xrange(grid.shape[0]-len(fullLines), grid.shape[0]):
		grid[r,:].fill(0)

class Board():
	def __init__(self, grid = np.zeros((6, 6), np.int8), linesCompleted = 0):
		self.rows = grid.shape[0]
		self.cols = grid.shape[1]
		self.grid = grid
		self.linesCompleted = linesCompleted
		
	def extractContour(self, border):
		contour = [0]
		for c in xrange(1, border.shape[0]):
			contour.append(border[c] - border[0])
		return contour
	
	def alignContour(self, bottomContour, topContour):
		outputs = []
		for i in xrange(len(bottomContour) - len(topContour) + 1):
			diff = [0] + [topContour[j] - (bottomContour[i+j] - bottomContour[i]) for j in xrange(1, len(topContour))]
			minDiff = min(diff)
			outputs.append(minDiff)
		return outputs

	def printScreen(self):
		self.printBoard(self.grid)
	
	def printBoard(self, board):
		for row in board:
			for col in row:
				print col
			
	def tryPlacing(self, pieceGrid):
		maxCols = findBorder(self.grid)
		contour = self.extractContour(maxCols)
		
		minPieceCols = findBorder(pieceGrid, isTop = False)
		pieceContour = self.extractContour(minPieceCols)
		print contour
		print pieceContour
		
		alignments = self.alignContour(contour, pieceContour)
		print alignments
		shape = pieceGrid.shape
		placements = []
		for c, alignment in enumerate(alignments):
			newGrid = np.copy(self.grid)
			pos = (maxCols[c]-minPieceCols[0]-alignment+1, c)
			print pos
			newGrid[pos[0]:pos[0]+shape[0], pos[1]:pos[1]+shape[1]] += pieceGrid
			reward = tryRemoveLines(newGrid, pos[0], pos[0]+shape[0])
			placements.append((newGrid, reward))
		return placements
	
	def updateGrid(self, grid):
		self.grid = grid
				
if __name__ == "__main__":		
	board = Board()
	printGrid(board.grid)
	oPiece = OPiece()
	sPiece = SPiece()
	tPiece = TPiece()
	lPiece = LPiece()
	placements = board.tryPlacing(oPiece.getRotations()[0])
	board.updateGrid(placements[0][0])
	placements = board.tryPlacing(oPiece.getRotations()[0])
	board.updateGrid(placements[2][0])
	placements = board.tryPlacing(sPiece.getRotations()[0])
	board.updateGrid(placements[4][0])
	placements = board.tryPlacing(tPiece.getRotations()[1])
	board.updateGrid(placements[4][0])
	placements = board.tryPlacing(lPiece.getRotations()[1])
	for grid, reward in placements:
		printGrid(grid)
		print 'reward', reward
