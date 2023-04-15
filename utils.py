import numpy as np

def random_initial_grid(rows, cols, images):
    grid = np.zeros((rows, cols), dtype=int)
    image_keys = list(images.keys())

    for r in range(rows):
        for c in range(cols):
            if np.random.random() < 0.5:
                grid[r, c] = image_keys.index(np.random.choice(image_keys))

    return grid
