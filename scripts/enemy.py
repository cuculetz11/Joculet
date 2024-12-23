import pygame
import random
from scripts.entities import PhysicsEntity
from scripts.particle import Particle

class Enemy(PhysicsEntity):
    """
    Clasa ce o folosesc pentru inamic ce are urmatoarele functionalitati
    - daca in fata lui este gol, atunci se va intoarce
    - cand se opreste din mers, ataca
    - ceea ce sunt implementari lejere adica nu sunt foarte complexe
    - as putea spune ca e un inamic "prost" :))
    """
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)
        self.health = 2
        self.walking = 0

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
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

            # cand se opreste din mers, ataca
            if not self.walking:
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                if (abs(dis[1]) < 16): # daca distanta dintre player si enemy e mai mica de 16 pixeli, atunci impusca
                    if (self.flip and dis[0] < 0): # verific daca e cu fata
                        self.game.sfx['shoot'].play()
                        self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -2, 0])
                    if (not self.flip and dis[0] > 0):
                        self.game.sfx['shoot'].play()
                        self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 2, 0])
                                                                             #[X,Y], directia/viteza, timer                  


        elif random.random() < 0.01: # daca nu merge, alege alta directie (1% sansa)
            
            self.walking = random.randint(45, 140)

        super().update(tilemap, movement=movement)

        # setetam animatia in functie de miscare
        if movement[0] != 0:
            self.set_action('enemy/run')
        else:
            self.set_action('enemy/idle')

        if abs(self.game.player.dashing) >= 60:
                if self.rect().colliderect(self.game.player.rect()):
                    self.game.sfx['hit'].play()
                    self.game.enemies.remove(self)
                    #self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[0, 0], frame=random.randint(0, 7), life=20))
                    #                 
   
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

        # pune shuriken ul in mana
        # if self.flip:
        #     surf.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - 3 - self.game.assets['gun'].get_width() - offset[0], self.rect().centery - offset[1] - 2)) #roteste toata imaginea
        # else:
        #     surf.blit(self.game.assets['gun'], (self.rect().centerx + 3 - offset[0], self.rect().centery - offset[1] - 2))

