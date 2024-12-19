import pygame
import os

BASE_IMG_PATH = 'data/images/'


def load_image(name):
    img = pygame.image.load(BASE_IMG_PATH + name).convert()
    img.set_colorkey((0, 0, 0))
    return img

#aici putem face o functie ce incarca automat toate pozele dintr un director pe care le vrem
def load_images(path):
    images = []

    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images    
