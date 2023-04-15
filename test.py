import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def init_grid(rows, cols, random_seed=None):
    if random_seed:
        np.random.seed(random_seed)
    return np.random.choice([0, 1], size=(rows, cols), p=[0.5, 0.5])

def count_neighbors(grid, row, col):
    neighbors = [(i, j) for i in range(row - 1, row + 2)
                 for j in range(col - 1, col + 2)
                 if (i, j) != (row, col)]
    count = 0
    for i, j in neighbors:
        if i >= 0 and i < grid.shape[0] and j >= 0 and j < grid.shape[1]:
            count += grid[i, j]
    return count

def next_generation(grid):
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            num_neighbors = count_neighbors(grid, i, j)
            if grid[i, j] == 1 and (num_neighbors < 2 or num_neighbors > 3):
                new_grid[i, j] = 0
            elif grid[i, j] == 0 and num_neighbors == 3:
                new_grid[i, j] = 1
    return new_grid

def update(frame_number, img, grid):
    new_grid = next_generation(grid)
    img.set_data(new_grid)
    grid[:] = new_grid[:]

def main():
    rows, cols = 50, 50
    grid = init_grid(rows, cols)
    fig, ax = plt.subplots()
    img = ax.imshow(grid, cmap='gray', interpolation='nearest')
    ani = FuncAnimation(fig, update, fargs=(img, grid), interval=100, save_count=50)
    plt.show()

if __name__ == '__main__':
    main()
