import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import concurrent.futures

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

def process_chunk(grid, new_grid, row_start, row_end):
    for i in range(row_start, row_end):
        for j in range(grid.shape[1]):
            num_neighbors = count_neighbors(grid, i, j)
            if grid[i, j] == 1 and (num_neighbors < 2 or num_neighbors > 3):
                new_grid[i, j] = 0
            elif grid[i, j] == 0 and num_neighbors == 3:
                new_grid[i, j] = 1

def next_generation(grid, num_threads=4):
    new_grid = grid.copy()
    chunk_size = grid.shape[0] // num_threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_chunk, grid, new_grid, i * chunk_size, (i + 1) * chunk_size) for i in range(num_threads)]
        concurrent.futures.wait(futures)
    return new_grid

def update(frame_number, grid, images, ax):
    new_grid = next_generation(grid)
    ax.clear()
    ax.set_xlim(0, grid.shape[1])
    ax.set_ylim(0, grid.shape[0])

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            cell = new_grid[i, j]
            if cell == 1:
                image = images[0]
                imagebox = OffsetImage(image, zoom=0.5)
                ab = AnnotationBbox(imagebox, (j, i), frameon=False, box_alignment=(0, 0))
                ax.add_artist(ab)
    grid[:] = new_grid[:]
    ax.axis('off')

def load_images(directory):
    valid_exts = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    file_list = sorted([file for file in os.listdir(directory) if file.lower().endswith(valid_exts)])
    images = [Image.open(os.path.join(directory, file)) for file in file_list]
    return [np.asarray(image.convert('RGBA')) for image in images]

def main():
    rows, cols = 50, 50
    grid = init_grid(rows, cols)
    images = load_images('conway')
    
    if len(images) < 1:
        raise ValueError("At least one image is required in the 'conway' directory for live cells.")

    fig, ax = plt.subplots()
    ani = FuncAnimation(fig, update, fargs=(grid, images, ax), interval=100, save_count=50)
    
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    main()

