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
	return fullLines
	
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
		self.border = findBorder(self.grid)
		self.holes = self.countHoles()
		
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
		
		maxCols = self.border
		contour = self.extractContour(maxCols)
		
		minPieceCols = findBorder(pieceGrid, isTop = False)
		pieceContour = self.extractContour(minPieceCols)
		
		alignments = self.alignContour(contour, pieceContour)
		shape = pieceGrid.shape
		placements = []
		for c, alignment in enumerate(alignments):
			newGrid = np.copy(self.grid)
			pos = (maxCols[c]-minPieceCols[0]-alignment+1, c)
# 			print pos, shape
			if pos[0] + shape[0] <= self.rows:
				newGrid[pos[0]:pos[0]+shape[0], pos[1]:pos[1]+shape[1]] += pieceGrid
				fullLines = tryRemoveLines(newGrid, pos[0], pos[0]+shape[0])
				linesCleared = len(fullLines)
				fullLines -= pos[0]
				if len(fullLines) != 0:
					nCellsRemoved = np.sum(pieceGrid[fullLines])
				else:
					nCellsRemoved = 0
				placements.append((newGrid, linesCleared, nCellsRemoved, pos[0] + shape[0]*0.5))
		return placements
	
	def __hash__(self):
		return self.h.__hash__()
	
	def __eq__(self, other):
		return np.array_equal(self.grid, other.grid)
	
	def updateGrid(self, grid):
		self.grid = grid
		self.h = util.gridHash(grid)
		self.border = findBorder(self.grid)
		self.holes = self.countHoles()
		
	def findHeightDiffs(self):
		diffs = []
		for col in xrange(1, self.cols):
			diffs.append(self.border[col] - self.border[col-1])
		return diffs
		
	def findMaxHeight(self):
		return max(self.border) + 1
		
	def findHeightGap(self):
		boardBorder = self.border
		highest = max(boardBorder)
		lowest = min(boardBorder)
		return highest - lowest
	
	def findDensity(self):
		nNonzero = np.count_nonzero(self.grid)
		sz = self.cols * self.findMaxHeight()
		return float(nNonzero) / sz if sz > 0 else 1
		
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
		return sum(self.border)/self.cols
	
	def countHoles(self):
		holes = 0
		for col in xrange(self.cols):
			holes += np.sum(self.grid[:self.border[col],col])
		return holes
	
	def countRowTransitions(self):
		#rowTransitions = 2 * (self.rows - max(self.border) - 1)
		rowTransitions = 0
		for row in xrange(self.rows):
			if self.grid[row,0] == 0:
				rowTransitions += 1
			for col in xrange(1, self.cols):
				if self.grid[row,col] != self.grid[row,col-1]:
					rowTransitions += 1
			if self.grid[row,self.cols-1] == 0:
				rowTransitions += 1
		return rowTransitions
	
	def countColTransitions(self):
		colTransitions = 0
		for col in xrange(self.cols):
			if self.grid[0,col] == 0:
				colTransitions += 1
			for row in xrange(1, self.rows):
				if self.grid[row,col] != self.grid[row-1,col]:
					colTransitions += 1
			if self.grid[self.rows-1,col] == 0:
				colTransitions += 1
		return colTransitions
	
	def getUnderHoles(self, row, col):
		depth = 0
		for curRow in reversed(xrange(row+1)):
			if self.grid[curRow, col]:
				return depth
			else:
				depth += 1
		return depth
		
	def extraFeatures(self):
		holes = 0
		wells = 0
		weightedHoles = 0
		highestHole = 0
		deepestHole = self.rows
		filled = 0
		weightedFilled = 0
		border = findBorder(self.grid)
		rowsWithHoles = set()
		for col in xrange(self.cols):
			wellCount = 0
			for row in xrange(border[col]):
				if self.grid[row,col] == 0:
					holes += 1
					rowsWithHoles.add(row)
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
		
		wellValue = 0
		holeDepth = 0
		for col in xrange(self.cols):
			pile = 0
			for row in reversed(xrange(self.cols)):
				cellLeft = self.grid[row,col-1] if col >= 1 else 1
				cellRight = self.grid[row,col+1] if col < self.cols-1 else 1
				if cellLeft and cellRight:
					wellValue += self.getUnderHoles(row, col)
				if self.grid[row,col]:
					pile += 1
				else:
					holeDepth += pile
					pile = 0
			
		hasHole = (holes >= 1)
		has2Holes = (holes >= 2)
		has4Holes = (holes >= 4)
		has8Holes = (holes >= 8)
		has16Holes = (holes >= 16)
# 		return (hasHole, has2Holes, has4Holes, has8Holes, has16Holes, holes, wells, weightedHoles, highestHole, deepestHole, filled, weightedFilled)
# 		return (hasHole, has2Holes, has4Holes, has8Holes, has16Holes, 0, 0, 0, 0, 0, 0, 0)
		return (0, 0, 0, 0, 0, holes, 0, 0, 0, 0, 0, 0, wellValue, holeDepth, len(rowsWithHoles))
	
	def DellacherieFeatures(self):		
		wellValue = 0
		holeDepth = 0
		for col in xrange(self.cols):
			pile = 0
			for row in reversed(xrange(self.cols)):
				cellLeft = self.grid[row,col-1] if col >= 1 else 1
				cellRight = self.grid[row,col+1] if col < self.cols-1 else 1
				if cellLeft and cellRight:
					wellValue += self.getUnderHoles(row, col)
				if self.grid[row,col]:
					pile += 1
				else:
					holeDepth += pile
					pile = 0
		return (wellValue, holeDepth)
				
if __name__ == "__main__":		
	board = Board()
	util.printGrid(board.grid)
	iPiece = IPiece()
	oPiece = OPiece()
	sPiece = SPiece()
	tPiece = TPiece()
	lPiece = LPiece()
	placements = board.tryPlacing(oPiece.getRotations()[0])
	board.updateGrid(placements[0][0])
	placements = board.tryPlacing(oPiece.getRotations()[0])
	board.updateGrid(placements[2][0])
	placements = board.tryPlacing(oPiece.getRotations()[0])
	board.updateGrid(placements[4][0])
	placements = board.tryPlacing(oPiece.getRotations()[0])
	board.updateGrid(placements[8][0])
	placements = board.tryPlacing(oPiece.getRotations()[0])
	board.updateGrid(placements[0][0])
	placements = board.tryPlacing(sPiece.getRotations()[0])
	for grid, reward, nCellsRemoved in placements:
		util.printGrid(grid)
		print 'reward', reward, nCellsRemoved
		#print 'horRough', board.getHorizontalRoughness(grid)
		#print 'verRough', board.getVerticalRoughness(grid)
