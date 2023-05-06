import numpy as np

def vertical_update(grid, live_cell_percentage, audio_level, row_directions):
    rows, cols = grid.shape

    speed = 0.08
    shift = int(speed * audio_level)

    new_grid = np.zeros_like(grid)

    for r in range(rows):
        if row_directions[r] == 1:
            new_grid[r] = np.roll(grid[r], -shift)
        else:
            new_grid[r] = np.roll(grid[r], shift)

    return new_grid
