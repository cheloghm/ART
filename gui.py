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

    # Get the current screen resolution
    screen_info = pygame.display.Info()
    max_screen_width = screen_info.current_w
    max_screen_height = screen_info.current_h

    # Calculate the number of rows and columns
    num_rows = max_screen_height // image_height
    num_cols = max_screen_width // image_width

    # Calculate the actual screen width and height based on the number of rows and columns
    screen_width = image_width * num_cols
    screen_height = image_height * num_rows

    # Create a window with the screen resolution size
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    # Create initial grid with 10% live cells
    grid = random_initial_grid(num_rows, num_cols, images)

    # Game loop
    running = True
    last_update_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
                grid = update_grid(grid)
                if audio_level > 0:
                    grid = generate_new_live_cells(grid, images, live_probability=audio_level / 100)
                    grid = randomly_kill_cells(grid, probability=(100 - audio_level) / 100)
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
