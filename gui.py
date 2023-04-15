import pygame
import numpy as np
from game_of_life import update_grid
from audio import get_audio_level
from image_loader import load_and_resize_images
from utils import random_initial_grid

def run_app():
    # Initialize pygame and create a window
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    # Load images
    images = load_and_resize_images("conway")

    # Create initial grid
    grid = random_initial_grid(20, 15, images)

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get audio level
        audio_level = get_audio_level()

        # Update grid based on audio level
        if audio_level > 0:
            grid = update_grid(grid)

        # Draw the grid
        draw_grid(screen, grid, images)

        # Update display
        pygame.display.flip()

    pygame.quit()

def draw_grid(screen, grid, images):
    cell_width = screen.get_width() // grid.shape[1]
    cell_height = screen.get_height() // grid.shape[0]
    image_keys = list(images.keys())

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            cell_value = grid[r, c]
            if cell_value:
                image_key = image_keys[cell_value]
                image = images[image_key]
                screen.blit(image, (c * cell_width, r * cell_height))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (c * cell_width, r * cell_height, cell_width, cell_height))

    for r in range(grid.shape[0]):
        pygame.draw.line(screen, (50, 50, 50), (0, r * cell_height), (screen.get_width(), r * cell_height))

    for c in range(grid.shape[1]):
        pygame.draw.line(screen, (50, 50, 50), (c * cell_width, 0), (c * cell_width, screen.get_height()))

