import numpy as np

def random_initial_grid(num_rows, num_cols, images, live_probability=0.15):
    grid = np.empty((num_rows, num_cols), dtype=object)
    image_keys = list(images.keys())
    for r in range(num_rows):
        for c in range(num_cols):
            if np.random.random() < live_probability:
                grid[r, c] = np.random.choice(image_keys)
            else:
                grid[r, c] = ''
    return grid

def generate_new_live_cells(grid, images, live_cell_percentage=0.85):
    num_rows, num_cols = grid.shape
    num_cells = num_rows * num_cols
    num_live_cells = int(live_cell_percentage * num_cells)
    num_dead_cells = num_cells - num_live_cells

    live_cells_positions = np.random.choice(num_cells, num_live_cells, replace=False)
    dead_cells_positions = np.random.choice(num_cells, num_dead_cells, replace=False)
    flat_grid = np.array([''] * num_cells, dtype=object)

    for pos in live_cells_positions:
        flat_grid[pos] = np.random.choice(list(images.keys()))

    for pos in dead_cells_positions:
        flat_grid[pos] = ''

    return flat_grid.reshape((num_rows, num_cols))
