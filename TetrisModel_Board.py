#
#	Authors:	BrianTruong
#					PatricioFigueroa
#
#	Tetris Model: Board (Screen)
#

import sys
import numpy as np
from copy import deepcopy
from TetrisModel_Pieces import *

def findBorder(a, isTop = True):
	border = np.empty((a.shape[1]), np.int8)
	border.fill(-1)
	for c in xrange(a.shape[1]):
		# search from top if isTop and from bottom otherwise
		searchedRange = xrange(a.shape[0]-1,-1,-1) if isTop else xrange(a.shape[0])
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
	def __init__(self, grid = np.zeros((20, 10), np.int8), linesCompleted = 0, nPieces = 0):
		self.rows = grid.shape[0]
		self.cols = grid.shape[1]
		self.grid = grid
		self.linesCompleted = linesCompleted
		self.nPieces = nPieces
		self.h = util.gridHash(grid)
		
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
			
	def tryPlacing(self, piece):
		pieceGrid = piece.grid
		
		maxCols = findBorder(self.grid)
		contour = self.extractContour(maxCols)
		
		minPieceCols = findBorder(pieceGrid, isTop = False)
		pieceContour = self.extractContour(minPieceCols)
# 		print contour
# 		print pieceContour
		
		alignments = self.alignContour(contour, pieceContour)
# 		print alignments
# 		printGrid(self.grid)

# 		printGrid(pieceGrid)
		shape = pieceGrid.shape
		placements = []
		for c, alignment in enumerate(alignments):
			newGrid = np.copy(self.grid)
			pos = (maxCols[c]-minPieceCols[0]-alignment+1, c)
# 			print pos, shape
			if pos[0] + shape[0] <= self.rows:
				newGrid[pos[0]:pos[0]+shape[0], pos[1]:pos[1]+shape[1]] += pieceGrid
				reward = tryRemoveLines(newGrid, pos[0], pos[0]+shape[0])
				placements.append((newGrid, reward))
		return placements
	
	def __hash__(self):
		return self.h.__hash__()
	
	def __eq__(self, other):
		return np.array_equal(self.grid, other.grid)
	
	def updateGrid(self, grid):
		self.grid = grid
		self.h = util.gridHash(grid)
		
	def findMaxHeight(self):
		return max(findBorder(self.grid)) + 1
		
	def findHeightGap(self):
		boardBorder = findBorder(self.grid)
		highest = max(boardBorder)
		lowest = min(boardBorder)
		return highest - lowest
		
	def getHorizontalRoughness(self):
		changes = 0;
		val = self.grid[0][0]
		for i in xrange(self.rows):
			for j in xrange(self.cols):
				if val != self.grid[i][j]:
					val = self.grid[i][j]
					changes += 1		
		return changes
		
	def getVerticalRoughness(self):
		changes = 0;
		val = self.grid[0][0]
		for j in xrange(self.cols):
			for i in xrange(self.rows):
				if val != self.grid[i][j]:
					val = self.grid[i][j]
					changes += 1		
		return changes	
	
	def findAvgHeight(self):
		return sum(findBorder(self.grid))/self.cols
	
	def countHoles(self):
		border = findBorder(self.grid)
		c = 0
		for col in xrange(self.cols):
			for row in xrange(border[col]):
				if self.grid[row,col] == 0:
					c += 1
		return c
		
	def extraFeatures(self):
		holes = 0
		wells = 0
		weightedHoles = 0
		highestHole = 0
		deepestHole = self.rows
		filled = 0
		weightedFilled = 0
		border = findBorder(self.grid)
		for col in xrange(self.cols):
			wellCount = 0
			for row in xrange(border[col]):
				if self.grid[row,col] == 0:
					holes += 1
					weightedHoles += row
					if deepestHole > row:
						deepestHole = row
					if highestHole < row:
						highestHole = row
					wellCount += 1
					if wellCount == 3:
						wells += 1
				else:
					wellCount = 0
					filled += 1
					weightedFilled += row
			
		return (holes, wells, weightedHoles, highestHole, deepestHole, filled, weightedFilled)
				
if __name__ == "__main__":		
	board = Board()
	util.printGrid(board.grid)
	oPiece = OPiece()
	sPiece = SPiece()
	tPiece = TPiece()
	lPiece = LPiece()
	placements = board.tryPlacing(oPiece.getRotations()[0])
	board.updateGrid(placements[0][0])
	placements = board.tryPlacing(oPiece.getRotations()[0])
	board.updateGrid(placements[2][0])
	placements = board.tryPlacing(oPiece.getRotations()[0])
	board.updateGrid(placements[7][0])
	placements = board.tryPlacing(oPiece.getRotations()[0])
	board.updateGrid(placements[0][0])
	placements = board.tryPlacing(sPiece.getRotations()[0])
	for grid, reward in placements:
		util.printGrid(grid)
		print 'reward', reward
		#print 'horRough', board.getHorizontalRoughness(grid)
		#print 'verRough', board.getVerticalRoughness(grid)
