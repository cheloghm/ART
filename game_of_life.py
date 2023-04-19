import numpy as np

def update_grid(grid):
    num_rows, num_cols = grid.shape
    new_grid = np.empty((num_rows, num_cols), dtype=object)

    for r in range(num_rows):
        for c in range(num_cols):
            neighbors = count_neighbors(grid, r, c)
            cell_value = grid[r, c]

            if cell_value == '':
                if neighbors == 3:
                    new_grid[r, c] = np.random.choice(list(grid.flatten()))
                else:
                    new_grid[r, c] = ''
            else:
                if neighbors < 2 or neighbors > 3:
                    new_grid[r, c] = ''
                else:
                    new_grid[r, c] = cell_value

    return new_grid

def count_neighbors(grid, r, c):
    num_rows, num_cols = grid.shape
    live_neighbors = 0

    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue

            nr, nc = r + dr, c + dc

            if 0 <= nr < num_rows and 0 <= nc < num_cols:
                if grid[nr, nc] != '':
                    live_neighbors += 1

    return live_neighbors

def randomly_kill_cells(grid, probability=0.1):
    num_rows, num_cols = grid.shape

    for r in range(num_rows):
        for c in range(num_cols):
            if np.random.random() < probability and grid[r, c] != '':
                grid[r, c] = ''

    return grid
