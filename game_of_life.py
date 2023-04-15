import numpy as np

def update_grid(grid):
    new_grid = grid.copy()
    rows, cols = grid.shape
    
    for r in range(rows):
        for c in range(cols):
            neighbors = np.sum(grid[r-1:r+2, c-1:c+2]) - grid[r, c]
            if grid[r, c] and (neighbors < 2 or neighbors > 3):
                new_grid[r, c] = 0
            elif not grid[r, c] and neighbors == 3:
                new_grid[r, c] = 1
                
    return new_grid
