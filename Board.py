import sys
from copy import deepcopy
from Pieces import *

class Board():
	def __init__(self, rows = 20, cols = 8):
		#print "New Board! (%dx%d)" % (rows, cols)
		self.rows = rows
		self.cols = cols
		self.board = [[0] * cols for i in range(rows)]
		self.Hlev = rows
		self.linesCompleted = 0

	def printScreen(self):
		self.printBoard(self.board)
	
	def printBoard(self, board):
		for row in board:
			for col in row:
				sys.stdout.write(str(col) + " ") 
			sys.stdout.write("\n") 
			
	def tryPlacing(self, pieceData, bester):
		piece, pRows, pCols = pieceData
		#print 'estamos hablando de %d columnas' % pCols, self.Hlev
		bestPlacement, bestHeight = bester
		for j in range(0, self.cols - pCols + 1):
			#print "====>", 
			floor = True
			for i in range(self.Hlev-pRows, self.rows - pRows + 1):
				#print i, self.rows - pRows + 1
				if not self.noOverlap(pieceData, i, j):
					#print 'Cai'
					floor = False
					break
			if not floor:
				i -= 1
			if i < 0:
				break
			#print "Posicion %d-%d" % (i,j)
				#print self.noOverlap(pieceData, i, j)
			result = self.placePiece(pieceData, i, j)
			if result is None:
				break
			self.checkForLines(result)
			height = self.checkHeight(result)
			#print '==>', height
			#self.printBoard(result)
			if height > bestHeight:
				bestHeight = height
				bestPlacement = result
		return (bestPlacement, bestHeight)
				#break
		
	def noOverlap(self, pieceData, posX, posY):
		piece, pRows, pCols = pieceData
		for i in range(pRows):
			for j in range(pCols):
				if piece[i][j] == 1 and self.board[posX + i][posY + j] == 1:
					return False
		return True
		
	def placePiece(self, pieceData, posX, posY):
		piece, pRows, pCols = pieceData
		copyBoard = deepcopy(self.board)
		for i in range(pRows):
			for j in range(pCols):
				copyBoard[posX+i][posY+j] += piece[i][j]
				if copyBoard[posX+i][posY+j] > 1:
					return None
		return copyBoard
		
	def checkHeight(self, board):
		for i in range(self.rows-1,0-1,-1):
			emptyRow = True
			for j in range(self.cols):	
				if board[i][j] > 0:
					emptyRow = False
			if emptyRow:
				return i+1
		return -1
		
	def updateBoard(self, bestBoard):
		bestScreen, bestHeight = bestBoard
		self.board = bestScreen
		self.Hlev = bestHeight
				
	def checkForLines(self, board):
		for i in range(self.rows-1,0-1,-1):
			lineFull = True
			while lineFull:
				for j in range(self.cols):
					#print "(%d,%d)" % (i,j)
					if board[i][j] != 1:
						lineFull = False
				if lineFull:
					#print 'Hay q borrar la linea %d' % i
					self.removeLine(board, i)
		
	def removeLine(self, board, line):
		self.linesCompleted += 1
		for i in range(line,0, -1):
			for j in range(self.cols):
				board[i][j] = board[i-1][j]
		board[0] = [0] * self.cols