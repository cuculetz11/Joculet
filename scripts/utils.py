import pygame
import os

BASE_IMG_PATH = 'data/images/'


def load_image(name):
    img = pygame.image.load(BASE_IMG_PATH + name).convert()
    img.set_colorkey((0, 0, 0))
    return img

# aici putem face o functie ce incarca automat toate pozele dintr-un director pe care le vrem
def load_images(path):
    images = []

    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images    

class Animation:
    """
    Aceasta clasa reprezinta o animatie
    Args:   images - lista de imagini ce reprezinta animatia
            img_dur - durata fiecarei imagini(cate frameuri sa stea pe ecran(de exemplu cum eu am setat la 70 de fps, 5 inseamna ca o imagine va sta pe ecran 5/70 secunde))
            loop - daca animatia se repeta sau nu
    """
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.img_dur = img_dur
        self.loop = loop
        self.frame = 0  # reprezinta un contor ce ne ajuta sa stim ce imagine sa afisam
        self.done = False

    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)
    
    def img(self):
        return self.images[int(self.frame / self.img_dur)] # returneaza imaginea curenta
    # frame = i(indexul imaginii) * durata imaginii pe frameuri
    # acest frame creste la fiecare cadru si practic datorita acestuia putem sa stim ce imagine sa afisam
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (len(self.images) * self.img_dur) # ne folosim de % pentru a face animatia sa se repete
        else:
            self.frame = min(self.frame + 1, len(self.images) * self.img_dur - 1)
            if self.frame == len(self.images) * self.img_dur - 1:
                self.done = True
            #nr maxim de frameuri este nr de img * durata fiecarei imagini pe frameuri