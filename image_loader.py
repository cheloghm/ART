import os
import pygame
from PIL import Image

def load_conway_images(size=None):  # Add the 'size' parameter with a default value of None
    directory = "conway"
    images = {}
    extensions = ['.png', '.jpeg', '.jpg']

    for file in os.listdir(directory):
        if any(file.lower().endswith(ext) for ext in extensions):
            img = Image.open(os.path.join(directory, file))
            if size:  # Add this condition to check if a size is provided
                img_resized = img.resize(size)
            else:
                img_resized = img
            img_surface = pygame.image.fromstring(img_resized.tobytes(), img_resized.size, img_resized.mode)
            images[file] = img_surface

    return images
