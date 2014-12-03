#
#	Authors:	BrianTruong
#					PatricioFigueroa
#
#	Tetris Model: Tetrominoes (Pieces)
#

import numpy as np
import util

class Piece():
	def __init__(self, grid=None, id=0):
		if grid is None:
			grid, id = self.createBase()
		self.grid = grid
		self.h = util.gridHash(grid)
		self.id = id
		
	def __hash__(self):
		return self.h.__hash__()
	
	def __eq__(self, other):
		return self.h == other.h
	
	@classmethod
	def createBase(cls):
		raise NotImplementedError()
	
	@classmethod
	def createRotations(cls):
		base, id = cls.createBase()
		outputs = [Piece(base)]
		while True:
			rotated = np.rot90(outputs[-1].grid)
			if not np.array_equal(rotated, base):
				outputs.append(Piece(rotated))
			else:
				break
		return outputs
	
	@classmethod
	def getRotations(cls):
		if cls.rotations is None:
			cls.rotations = cls.createRotations()	
		return cls.rotations 
	
class OPiece(Piece):
	base = None
	rotations = None
	
	@classmethod
	def createBase(cls):
		if cls.base is None:
			#print "O"
			cls.base = np.ones((2, 2), np.int8)
		return (cls.base, 1)
	
class IPiece(Piece):
	base = None
	rotations = None
	
	@classmethod
	def createBase(cls):
		if cls.base is None:
			#print "I"
			cls.base = np.ones((1, 4), np.int8)
		return (cls.base, 2)
	
class TPiece(Piece):
	base = None
	rotations = None
	
	@classmethod
	def createBase(cls):
		if cls.base is None:
			#print "T"
			cls.base = np.ones((2, 3), np.int8)
			cls.base[0,0] = 0
			cls.base[0,2] = 0
		return (cls.base,3)
		
class SPiece(Piece):
	base = None
	rotations = None
	
	@classmethod
	def createBase(cls):
		if cls.base is None:
			#print "S"
			cls.base = np.ones((3, 2), np.int8)
			cls.base[0,0] = 0
			cls.base[2,1] = 0
		return (cls.base, 4)
		
class ZPiece(Piece):
	base = None
	rotations = None
	
	@classmethod
	def createBase(cls):
		if cls.base is None:
			#print "Z"
			cls.base = np.ones((3, 2), np.int8)
			cls.base[0,1] = 0
			cls.base[2,0] = 0
		return (cls.base,5)
		
class LPiece(Piece):
	base = None
	rotations = None
	
	@classmethod
	def createBase(cls):
		if cls.base is None:
			#print "L"
			cls.base = np.ones((3, 2), np.int8)
			cls.base[1,1] = 0
			cls.base[2,1] = 0
		return (cls.base,6)
		
class JPiece(Piece):
	base = None
	rotations = None
	
	@classmethod
	def createBase(cls):
		if cls.base is None:
			#print "J"
			cls.base = np.ones((3, 2), np.int8)
			cls.base[1,0] = 0
			cls.base[2,0] = 0
		return (cls.base,7)
		
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

def pieceByName(name):
	if name == 'O':
		return OPiece()
	elif name == 'I':
		return IPiece()
	elif name == 'T':
		return TPiece()
	elif name == 'S':
		return SPiece()
	elif name == 'Z':
		return ZPiece()
	elif name == 'L':
		return LPiece()
	elif name == 'J':
		return JPiece()
	return None

defaultList = [IPiece(), OPiece(), TPiece(), SPiece(), ZPiece(), LPiece(), JPiece()]

if __name__ == "__main__":
	l = [IPiece(), OPiece(), TPiece(), SPiece(), ZPiece(), LPiece(), JPiece()]
	for x in l:
		print x, '(%d rotations)' % len(x.getRotations()), '[id=%d]' % x.id
		for rotation in x.getRotations():
			util.printGrid(rotation.grid)
