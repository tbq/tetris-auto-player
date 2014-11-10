import sys
import numpy as np

def printGrid(grid):
	print ''.join(['-'] * (grid.shape[1]+2))
	for r in reversed(xrange(grid.shape[0])):
		symbols = ['|'] + ['X' if val else ' ' for val in grid[r,:]] + ['|']
		print ''.join(symbols)
	print ''.join(['-'] * (grid.shape[1]+2))

class Piece():
	def __init__(self):		
		pass
	
	@classmethod
	def createBase(cls):
		raise NotImplementedError()
	
	@classmethod
	def createRotations(cls):
		base = cls.createBase()
		outputs = [base]
		while True:
			rotated = np.rot90(outputs[-1])
			if not np.array_equal(rotated, base):
				outputs.append(rotated)
			else:
				break
		return outputs
	
	@classmethod
	def getRotations(cls):
		if cls.rotations is None:
			cls.rotations = cls.createRotations()	
		return cls.rotations
	
	def printGrid(self, piecePos):
		for row in piecePos:
			for col in row:
				sys.stdout.write(str(col) + " ") 
			sys.stdout.write("\n") 
	
class OPiece(Piece):
	
	rotations = None
	
	@classmethod
	def createBase(cls):
		print "O"
		return np.ones((2, 2), np.int8)
	
class IPiece(Piece):
	
	rotations = None
	
	@classmethod
	def createBase(cls):
		print "I"
		return np.ones((1, 4), np.int8)
	
class TPiece(Piece):
	rotations = None
	
	@classmethod
	def createBase(cls):
		print "T"
		base = np.ones((2, 3), np.int8)
		base[0,0] = 0
		base[0,2] = 0
		return base
		
class SPiece(Piece):
	rotations = None
	
	@classmethod
	def createBase(cls):
		print "S"
		base = np.ones((3, 2), np.int8)
		base[0,0] = 0
		base[2,1] = 0
		return base
		
class ZPiece(Piece):
	rotations = None
	
	@classmethod
	def createBase(cls):
		print "Z"
		base = np.ones((3, 2), np.int8)
		base[0,1] = 0
		base[2,0] = 0
		return base
		
class LPiece(Piece):
	rotations = None
	
	@classmethod
	def createBase(cls):
		print "L"
		base = np.ones((3, 2), np.int8)
		base[1,1] = 0
		base[2,1] = 0
		return base
		
class JPiece(Piece):
	rotations = None
	
	@classmethod
	def createBase(cls):
		print "J"
		base = np.ones((3, 2), np.int8)
		base[1,0] = 0
		base[2,0] = 0
		return base	
		
def pieceById(id):
	if id == 0:
		oPiece = OPiece()
	elif id == 1:
		oPiece = IPiece()
	elif id == 2:
		oPiece = TPiece()
	elif id == 3:
		oPiece = SPiece()
	elif id == 4:
		oPiece = ZPiece()
	elif id == 5:
		oPiece = LPiece()
	else: # id == 6
		oPiece = JPiece()
	return oPiece
	
def pieceNameById(id):
	if id == 0:
		oPiece = 'O'
	elif id == 1:
		oPiece = 'I'
	elif id == 2:
		oPiece = 'T'
	elif id == 3:
		oPiece = 'S'
	elif id == 4:
		oPiece = 'Z'
	elif id == 5:
		oPiece = 'L'
	else: # id == 6
		oPiece = 'J'
	return oPiece

if __name__ == "__main__":
	l = [IPiece(), OPiece(), TPiece(), SPiece(), ZPiece(), LPiece(), JPiece()]
	for x in l:
		print len(x.getRotations())
		for rotation in x.getRotations():
			printGrid(rotation)
