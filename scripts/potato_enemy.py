import pygame
import random
from scripts.entities import PhysicsEntity
import math
from scripts.particle import Particle


class PotatoEnemy(PhysicsEntity):
    """
    Clasa ce o folosesc pentru inamic ce are urmatoarele functionalitati
    - daca in fata lui este gol, atunci se va intoarce
    - cand se opreste din mers, ataca
    - ceea ce sunt implementari lejere adica nu sunt foarte complexe
    - as putea spune ca e un inamic "prost" :))
    """
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)

        self.walking = 0

    def take_damage(self):
        self.game.enemies.remove(self)

    def update(self, tilemap, movement=(0, 0)):
        if self.walking:
            # daca in fata lui este gol, atunci se va intoarce
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)): 
                #practic de la mijlocul enemy-ului  ne uitam 7 pixeli in fata sau in spate si sub el daca exista un tile solid
                if (self.collisions['right'] or self.collisions['left']):
                    self.flip = not self.flip
                else:
                    movement = (-0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)                


        elif random.random() < 0.01: # daca nu merge, alege alta directie (1% sansa)
            
            self.walking = random.randint(45, 140)

        super().update(tilemap, movement=movement)

        # setetam animatia in functie de miscare
        if movement[0] != 0:
            self.set_action('potato_enemy/run')
        else:
            self.set_action('potato_enemy/idle')
        #daca playerul ataca prin dash il omoara pe dusman, daca il atinge fara sa fie in dash, ii scade viata
        if abs(self.game.player.dashing) >= 60: 
                if self.rect().colliderect(self.game.player.rect()):
                    self.game.sfx['hit'].play()
                    self.game.enemies.remove(self)
                    
        else:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.sfx['hit'].play()
                self.game.player.health -= 1
                if self.game.player.flip:
                    self.game.player.pos[0] = self.game.player.pos[0] + 30
                else:     
                    self.game.player.pos[0] = self.game.player.pos[0] - 30

                for i in range(20):
                        #exact acelasi lucru ca la dash numai ca am schimbat culoarea particulelor
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 0.5 + 0.5
                    pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                    self.game.particles.append(Particle( self.game, 'shoots',  self.game.player.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
                    
    
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
        if self.flip:
            surf.blit(pygame.transform.flip(self.game.assets['kunai'], True, False), (self.rect().centerx - 3 - self.game.assets['kunai'].get_width() - offset[0], self.rect().centery - offset[1] - 1)) #roteste toata imaginea
        else:
            surf.blit(self.game.assets['kunai'], (self.rect().centerx + 3 - offset[0], self.rect().centery - offset[1] - 1))

