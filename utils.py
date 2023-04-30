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

def generate_new_live_cells(grid, images, live_cell_percentage):
    num_rows, num_cols = grid.shape
    total_cells = num_rows * num_cols
    target_live_cells = int(live_cell_percentage * total_cells)
    current_live_cells = np.sum(grid != '')

    while current_live_cells < target_live_cells:
        r, c = np.random.randint(num_rows), np.random.randint(num_cols)
        if grid[r, c] == '':
            grid[r, c] = np.random.choice(list(images.keys()))
            current_live_cells += 1

    return grid


def kill_live_cells(grid, live_cell_percentage):
    num_rows, num_cols = grid.shape
    total_cells = num_rows * num_cols
    target_live_cells = int(live_cell_percentage * total_cells)
    current_live_cells = np.sum(grid != '')

    while current_live_cells > target_live_cells:
        r, c = np.random.randint(num_rows), np.random.randint(num_cols)
        if grid[r, c] != '':
            grid[r, c] = ''
            current_live_cells -= 1

    return grid

    num_rows, num_cols = grid.shape
    live_cell_count = np.count_nonzero(grid)
    num_cells_to_kill = int(live_cell_percentage * live_cell_count)

    live_cell_indices = np.argwhere(grid)
    np.random.shuffle(live_cell_indices)

    for i in range(min(num_cells_to_kill, len(live_cell_indices))):
        r, c = live_cell_indices[i]
        grid[r, c] = ''

    return grid
