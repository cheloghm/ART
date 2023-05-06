import pygame
import numpy as np
from game_of_life import update_grid
from audio import get_audio_level, audio_level_to_update_interval
from image_loader import load_conway_images
from utils import random_initial_grid, generate_new_live_cells, kill_live_cells
from game_of_life import update_grid, randomly_kill_cells, adjust_live_cells
import time
from horizontal import horizontal_update
from vertical import vertical_update
import cv2

def run_app():
    pygame.init()

    # Load images and resize to the desired size
    images = load_conway_images(size=(50, 50))

    # Set screen size based on image size
    image_width, image_height = next(iter(images.values())).get_size()

    # Get the current screen resolution and create a window with that size
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    # Calculate the number of rows and columns based on the screen resolution
    num_rows = screen_height // image_height
    num_cols = screen_width // image_width

    # Adjust screen dimensions to match the grid dimensions
    screen_width = num_cols * image_width
    screen_height = num_rows * image_height

    # Create a window with the adjusted screen dimensions
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    # Set fullscreen flag
    fullscreen = False

    # Create initial grid with 15% live cells
    grid = random_initial_grid(num_rows, num_cols, images, live_probability=0.15)

   # List of sequence functions and index to current one
    sequences = [update_grid, vertical_update, horizontal_update]
    current_sequence = 0

    # Game loop
    running = True
    last_update_time = time.time()
    # last_sequence_change_time = time.time()
    update_interval = 0.6  # 100 beats per minute corresponds to 0.6 seconds per beat

    prev_audio_level = 15  # Initial audio level, defined within the function

    # Initialize sequence variable and sequence change interval
    sequence = 0  # 0: Conway's Game of Life, 1: Vertical Movement, 2: Horizontal Movement
    last_sequence_change_time = time.time()
    sequence_change_interval = 0.2 * 60  # Change sequence every 5 minutes

    sequence_change = False  # Flag to indicate if the sequence has changed

    # Initialize row_directions and col_directions with random 1s and -1s
    row_directions = np.random.choice([1, -1], grid.shape[0])
    col_directions = np.random.choice([1, -1], grid.shape[1])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:  # Toggle full-screen mode with F key
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen_width, screen_height))
                elif event.key == pygame.K_c:  # Change sequence with C key
                    sequence = (sequence + 1) % 3
                    last_sequence_change_time = time.time()
                    sequence_change = True

        # Change sequence every 5 minutes
        current_time = time.time()
        if current_time - last_sequence_change_time > sequence_change_interval:
            sequence = (sequence + 1) % 3
            last_sequence_change_time = current_time
            sequence_change = True

        # Get audio level
        audio_level = get_audio_level()
        print(f"Audio level: {audio_level}")

        # Pause if audio level is <= 5, resume if > 5
        if audio_level <= 5:
            continue
        elif prev_audio_level <= 5 and audio_level > 5:
            last_update_time = time.time() - update_interval  # Force an update on resume

        # Update grid at a rate of 100 beats per minute
        if current_time - last_update_time > update_interval:
            # Adjust live cell percentage based on audio level
            if sequence in [1, 2]:  # Fill the screen with live cells if it's a vertical or horizontal sequence
                live_cell_percentage = 1.0
            elif audio_level >= 90 or sequence_change:  # Fill the screen with live cells if the sequence has changed
                live_cell_percentage = 1.0
                sequence_change = False  # Reset the sequence change flag
            else:
                live_cell_percentage = round(audio_level / 100, 2)
                
            # Adjust live cells to match the target live cell percentage
            current_live_cell_percentage = np.count_nonzero(grid) / (num_rows * num_cols)
            if current_live_cell_percentage < live_cell_percentage:
                grid = generate_new_live_cells(grid, images, live_cell_percentage - current_live_cell_percentage)
            elif current_live_cell_percentage > live_cell_percentage:
                grid = kill_live_cells(grid, current_live_cell_percentage - live_cell_percentage)

            # Calculate the speed based on the sound decibels
            speed = audio_level / 10

            # Generate direction arrays for rows and columns only if the sequence has changed
            if sequence_change:
                row_directions = np.random.choice([1, -1], size=num_rows)
                col_directions = np.random.choice([1, -1], size=num_cols)
                sequence_change = False  # Reset the sequence change flag

           # Apply the appropriate update function based on the current sequence
            if sequence == 0:  # Conway's Game of Life
                grid = update_grid(grid)
            elif sequence == 1:  # Vertical Movement
                grid = generate_new_live_cells(grid, images, 1.0)
                grid = vertical_update(grid, live_cell_percentage, audio_level, row_directions)
            elif sequence == 2:  # Horizontal Movement
                grid = generate_new_live_cells(grid, images, 1.0)
                grid = horizontal_update(grid, live_cell_percentage, audio_level, col_directions)
            
            prev_audio_level = audio_level
            last_update_time = current_time

        # Draw the grid
        screen.fill((0, 0, 0))
        draw_grid(screen, grid, images, cell_width=image_width, cell_height=image_height)
        pygame.display.flip()

    pygame.quit()

def draw_grid(screen, grid, images, cell_width, cell_height):
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            cell_value = grid[r, c]
            if cell_value:
                image = images[cell_value]
                screen.blit(image, (c * cell_width, r * cell_height))
