import os
import pygame
from PIL import Image

def load_and_resize_images(directory, size=(32, 32)):
    images = {}
    extensions = ['.png', '.jpeg', '.jpg']

    for file in os.listdir(directory):
        if any(file.lower().endswith(ext) for ext in extensions):
            img = Image.open(os.path.join(directory, file))
            img_resized = img.resize(size)
            img_surface = pygame.image.fromstring(img_resized.tobytes(), img_resized.size, img_resized.mode)
            images[file] = img_surface

    return images
