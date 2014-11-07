import sys

class Piece():
	def __init__(self):		pass
	def rotations(self):		pass
	def printPiece(self, piecePos):
		for row in piecePos:
			for col in row:
				sys.stdout.write(str(col) + " ") 
			sys.stdout.write("\n") 
	
class OPiece(Piece):
	def rotations(self):
		base = [
			[1,1],
			[1,1]
		]
		return [(base, 2, 2)]
		
class IPiece(Piece):
	def rotations(self):
		rots = []
		vert = [
			[1],
			[1],
			[1],
			[1]
		]
		rots.append((vert, 4, 1))
		hor = [[1,1,1,1]]
		rots.append((hor, 1, 4))
		return rots
		
class TPiece(Piece):
	def rotations(self):
		rots = []
		p1 = [
			[1,1,1],
			[0,1,0]
		]
		rots.append((p1, 2, 3))
		p2 = [
			[0,1],
			[1,1],
			[0,1]
		]
		rots.append((p2, 3, 2))
		p3 = [
			[0,1,0],
			[1,1,1]
		]
		rots.append((p3, 2, 3))
		p4 = [
			[1,0],
			[1,1],
			[1,0]
		]
		rots.append((p4, 3, 2))
		
		return rots
		
class SPiece(Piece):
	def rotations(self):
		rots = []
		p1 = [
			[0,1,1],
			[1,1,0]
		]
		rots.append((p1, 2, 3))	
		p2 = [
			[1,0],
			[1,1],
			[0,1]
		]
		rots.append((p2, 3, 2))
		
		return rots
		
class ZPiece(Piece):
	def rotations(self):
		rots = []
		p1 = [
			[1,1,0],
			[0,1,1]
		]
		rots.append((p1, 2, 3))	
		p2 = [
			[0,1],
			[1,1],
			[1,0]
		]
		rots.append((p2, 3, 2))
		
		return rots
		
class LPiece(Piece):
	def rotations(self):
		rots = []
		p1 = [
			[0,0,1],
			[1,1,1]
		]
		rots.append((p1, 2, 3))	
		p2 = [
			[1,0],
			[1,0],
			[1,1]
		]
		rots.append((p2, 3, 2))
		p3 = [
			[1,1,1],
			[1,0,0]
		]
		rots.append((p3, 2, 3))	
		p4 = [
			[1,1],
			[0,1],
			[0,1]
		]
		rots.append((p4, 3, 2))
		return rots
		
class JPiece(Piece):
	def rotations(self):
		rots = []
		p1 = [
			[1,1,1],
			[0,0,1]
		]
		rots.append((p1, 2, 3))	
		p2 = [
			[0,1],
			[0,1],
			[1,1]
		]
		rots.append((p2, 3, 2))
		p3 = [
			[1,0,0],
			[1,1,1]
		]
		rots.append((p3, 2, 3))	
		p4 = [
			[1,1],
			[1,0],
			[1,0]
		]
		rots.append((p4, 3, 2))
		return rots		
		
def pieceById(id):
	if id == 0:
		piece = OPiece()
	elif id == 1:
		piece = IPiece()
	elif id == 2:
		piece = TPiece()
	elif id == 3:
		piece = SPiece()
	elif id == 4:
		piece = ZPiece()
	elif id == 5:
		piece = LPiece()
	else: # id == 6
		piece = JPiece()
	return piece
	
def pieceNameById(id):
	if id == 0:
		piece = 'O'
	elif id == 1:
		piece = 'I'
	elif id == 2:
		piece = 'T'
	elif id == 3:
		piece = 'S'
	elif id == 4:
		piece = 'Z'
	elif id == 5:
		piece = 'L'
	else: # id == 6
		piece = 'J'
	return piece