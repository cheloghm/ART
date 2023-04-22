import pygame
import numpy as np
from game_of_life import update_grid
from audio import get_audio_level, audio_level_to_update_interval
from image_loader import load_conway_images
from utils import random_initial_grid, generate_new_live_cells
from game_of_life import update_grid, randomly_kill_cells
import time

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

    # Create initial grid
    num_rows = screen_height // image_height
    num_cols = screen_width // image_width
    grid = random_initial_grid(num_rows, num_cols, images, live_probability=0.15)

    # Game loop
    running = True
    last_update_time = time.time()

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

        # Get audio level
        audio_level = get_audio_level()
        print(f"Audio level: {audio_level}")

        # Calculate update interval based on audio level
        update_interval = audio_level_to_update_interval(audio_level)
        print(f"Update interval: {update_interval}")

        # Update grid based on update interval
        if update_interval is not None:
            current_time = time.time()

            if current_time - last_update_time > update_interval:
                # Apply Conway's game of life rules
                grid = update_grid(grid)

                # Adjust live cell percentage based on audio level
                if audio_level >= 90:
                    live_cell_percentage = 1.0
                elif audio_level > 15:
                    live_cell_percentage = round(audio_level / 100, 2)
                else:
                    live_cell_percentage = 0.15

                # Generate new live cells
                grid = generate_new_live_cells(grid, images, live_cell_percentage=live_cell_percentage)
                last_update_time = current_time

        # Draw the grid
        screen.fill((0, 0, 0))
        draw_grid(screen, grid, images, cell_width=image_width, cell_height=image_height)

        # Update display
        pygame.display.flip()

    pygame.quit()

def draw_grid(screen, grid, images, cell_width, cell_height):
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            cell_value = grid[r, c]
            if cell_value:
                image = images[cell_value]
                x = c * cell_width
                y = r * cell_height
                screen.blit(image, (x, y))
