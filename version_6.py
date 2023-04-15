import pygame
import pyaudio
import numpy as np
import os
import random

# Define constants
GRID_SIZE = 5
IMAGE_SIZE = 100
IMAGE_PADDING = 10
WINDOW_SIZE = GRID_SIZE * (IMAGE_SIZE + IMAGE_PADDING) + IMAGE_PADDING
FPS = 60

# Initialize Pygame
pygame.init()

# Set up the window
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.FULLSCREEN)
pygame.display.set_caption("Sound Grid")

# Load images from the 'grid_images' directory
images = []
for filename in os.listdir('grid_images'):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        image = pygame.image.load(os.path.join('grid_images', filename)).convert_alpha()
        image = pygame.transform.scale(image, (IMAGE_SIZE, IMAGE_SIZE))
        images.append(image)

# Initialize Pyaudio
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=4096)

# Define functions
def get_loudness():
    # Measure sound loudness on a scale from 1 to 100
    data = np.frombuffer(stream.read(1024), dtype=np.int16)
    return int(np.abs(data).mean() / 32767 * 100)

def rotate_image(image, angle):
    # Rotate image by given angle
    return pygame.transform.rotate(image, angle)

def draw_grid(images):
    # Draw the grid of images on the window
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = i * (IMAGE_SIZE + IMAGE_PADDING) + IMAGE_PADDING
            y = j * (IMAGE_SIZE + IMAGE_PADDING) + IMAGE_PADDING
            window.blit(images[i * GRID_SIZE + j], (x, y))

# Initialize variables
angles = [0] * len(images)
speeds = [0] * len(images)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Detect sound and update images
    loudness = get_loudness()
    if loudness > 0:
        for i in range(len(images)):
            angle = angles[i] + speeds[i]
            image = rotate_image(images[i], angle)
            window.blit(image, ((i % GRID_SIZE) * (IMAGE_SIZE + IMAGE_PADDING) + IMAGE_PADDING,
                                (i // GRID_SIZE) * (IMAGE_SIZE + IMAGE_PADDING) + IMAGE_PADDING))
            speeds[i] = loudness / 2 + random.randint(-10, 10)
            angles[i] = angle % 360
    else:
        draw_grid(images)

    # Update the display and wait for the next frame
    pygame.display.flip()
    clock.tick(FPS)

# Clean up resources
stream.stop_stream()
stream.close()
audio.terminate()
pygame.quit()
