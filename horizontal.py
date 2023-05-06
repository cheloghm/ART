import numpy as np

def horizontal_update(grid, live_cell_percentage, audio_level, col_directions):
    rows, cols = grid.shape

    speed = 0.08
    shift = int(speed * audio_level)

    new_grid = np.zeros_like(grid)

    for c in range(cols):
        if col_directions[c] == 1:
            new_grid[:, c] = np.roll(grid[:, c], -shift)
        else:
            new_grid[:, c] = np.roll(grid[:, c], shift)

    return new_grid
