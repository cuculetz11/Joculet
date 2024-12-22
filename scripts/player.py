
import random
import math
import pygame
from scripts.entities import PhysicsEntity
from scripts.particle import Particle

class Player(PhysicsEntity):
    def __init__(self, game, e_type, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0 # timpul in aer pentru a sti cand sa afisam animatia de saritura
        self.jumps = 1
        self.dashing = 0
        self.health = 3

    # suprascriem update-ul de la entitati pentru a aduga animatiile specifice playerului
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)
        self.air_time += 1

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 2 # resetam sariturile in momentul in care avem o coliziune cu pamantul

        if self.air_time > 4:
            self.set_action('jump')    
        elif movement[0] != 0:
            self.set_action('run')    
        else:
            self.set_action('idle')
            
        #reprezinta efectul ce apare la finalul dash ului de imprastiere a particulelor in forma de cerc
        if abs(self.dashing) in {70, 60}:
            # generam 20 de particule ce primesc o anumita viteaza si un unghi random
            for i in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))

        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1) # pe fiecare frame scadem cate 1 din dashing
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)

        #aici practic e logica miscarii in dash plus generarea particulelor pe orizontala   
        if abs(self.dashing) > 60:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8 # in primele cadre ale dash-ului, viteza creste semnificativ
            if abs(self.dashing) == 61:
                self.velocity[0] *= 0.1
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0] #acete particule primesc o viteza random pe oriizontala
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))   
       

        if self.velocity[0] > 0:
            self.velocity[0] = max(0, self.velocity[0] - 0.1)
        else:
            self.velocity[0] = min(0, self.velocity[0] + 0.1)
        #daca exitsa o viteza pe x o vom reduce pana la 0        

    def check_fall(self):
        if self.pos[1] > 350:
            self.health = 0
            self.game.load_level(3)
            self.game.player.health = 3

    def check_ramen(self):
        if self.rect().colliderect(pygame.Rect(int(self.game.ramen[0]) * 16, int(self.game.ramen[1]) * 16, 10, 10)):
            print("ramen")
    def check_info(self):
        if self.rect().colliderect(pygame.Rect(int(self.game.info[0]) * 16, int(self.game.info[1]) * 16, 10, 10)):
            print("info")              
    def jump(self):
        if self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5

    def dash(self):
        #pentru ca noi aici folosim o valoare ce e egala cu nr de frameuri pe secunda ca sa putem face un fel de cooldown, adica fiecare dash in sine dureaza 1 secunda
        if not self.dashing:
            if self.flip:
                self.dashing = -70
            else:
                self.dashing = 70  

    def render(self, surf, offset=(0, 0)):
        #practic daca fac dash nu randez playerul
        if abs(self.dashing) <= 60:
            super().render(surf, offset = offset) 
           