'''
Created on Nov 14, 2014

@author: BrianTruong
'''

def gridHash(grid):
    h = 0
    for elem in grid.flat:
        h = (h << 1) + elem
    return (h, grid.shape[0], grid.shape[1])