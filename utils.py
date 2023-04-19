import numpy as np

def random_initial_grid(num_rows, num_cols, images, live_cells_ratio=0.5):
    grid = np.empty((num_rows, num_cols), dtype=object)
    image_keys = list(images.keys())
    for r in range(num_rows):
        for c in range(num_cols):
            if np.random.random() < live_cells_ratio:
                grid[r, c] = np.random.choice(image_keys)
            else:
                grid[r, c] = ''
    return grid

import numpy as np

def generate_new_live_cells(grid, images, live_probability=0.5):
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == -1 and np.random.random() < live_probability:
                grid[r, c] = np.random.choice(list(images.keys()))
    return grid
