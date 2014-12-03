#
#	Authors:	BrianTruong
#					PatricioFigueroa
#
#	Tetris Utilities
#

import numpy as np
import util

def printGrid(grid):
	print ''.join(['-'] * (grid.shape[1]+2))
	for r in reversed(xrange(grid.shape[0])):
		symbols = ['|'] + ['X' if val else ' ' for val in grid[r,:]] + ['|']
		print ''.join(symbols)
	print ''.join(['-'] * (grid.shape[1]+2))
	
def gridHash(grid):
    h = 0
    for elem in grid.flat:
        h = (h << 1) + elem
    return (h, grid.shape[0], grid.shape[1])