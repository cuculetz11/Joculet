import pygame
import random
import math

from scripts.particle import Particle

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) #e mai usor de lucrat cu liste
        self.size = size
        self.velocity = [0, 0] # viteza derivivata pozitiei
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        self.action =''
        self.anim_offset = (-3, -3) #
        self.flip = False
        self.set_action('idle')

    def rect(self):
        """
        Face un dreptunghi ce reprezinta aceasta entitate pemtru a putea realiza apoi coliziuni
        Args: self- ce repezinta intanta acestei clase( diferenta fata de java )
        Returneaza: un dreptunghi ce reprezinta aceasta entitate
        """
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        """
        Se seteaza animatia ce trebuie afisata in momentul respectiv
        Args: action - string ce reprezinta actiunea ce trebuie afisata
        am denumti animatiile cu "_animation" pentru a le putea distinge de celelalte chestii
        """
        if self.action == action:
            return
        self.action = action
        self.animation = self.game.assets[action + '_animation'].copy()

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0] #miscarea pe axa x

        entity_rect = self.rect()

        for react in tilemap.physics_around(self.pos):
            if entity_rect.colliderect(react):
                if frame_movement[0] > 0:
                    entity_rect.right = react.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = react.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x # setam pozitia pe x astfel incat se azugura ca nu poate trece prin tile              

        self.pos[1] += frame_movement[1] #miscarea pe axa y
        entity_rect = self.rect()

        for react in tilemap.physics_around(self.pos):
            if entity_rect.colliderect(react):
                if frame_movement[1] > 0:
                    entity_rect.bottom = react.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = react.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        if movement[0] < 0:
            self.flip = True #daca miscarea pe axa x este negativa, atunci playerul se va intoarce
        if movement[0] > 0:
            self.flip = False

        self.velocity[1] = min(9, self.velocity[1] + 0.18)  #g ravitatie 9 reprezentand valoarea maxima a vitezei, celalata  0.1 reprezentand acceleratia
    
        if(self.collisions['down'] or self.collisions['up']):
            self.velocity[1] = 0 # resetam viteza pe axa y in momentul in care avem o coliziune
        self.animation.update() # actualizam animatia

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(),self.flip, False), (self.pos[0] + self.anim_offset[0] - offset[0], self.pos[1] + self.anim_offset[1] - offset[1]))
        #surf.blit(self.game.assets['player'], (self.pos[0]- offset[0], self.pos[1] - offset[1]))


class Player(PhysicsEntity):
    def __init__(self, game, e_type, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0 # timpul in aer pentru a sti cand sa afisam animatia de saritura
        self.jumps = 1
        self.dashing = 0

    # suprascriem update-ul de la entitati pentru a aduga animatiile specifice playerului
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)
        self.air_time += 1

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1 # resetam sariturile in momentul in care avem o coliziune cu pamantul

        if self.air_time > 4:
            self.set_action('jump')    
        elif movement[0] != 0:
            self.set_action('run')    
        else:
            self.set_action('idle')
        #pe asta sa ma uit mai tarziu
        if abs(self.dashing) in {60, 50}:
            for i in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))

        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1) # pe fiecare frame scadem cate 1 din dashing
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        #si aici ca observ ca e ff schimbat    
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))   
        #se realizeaza un cooldown pentru a nu putea face dash la infinit si se reduce viteza semnificativ

        if self.velocity[0] > 0:
            self.velocity[0] = max(0, self.velocity[0] - 0.1)
        else:
            self.velocity[0] = min(0, self.velocity[0] + 0.1)
        #daca exitsa o viteza pe x o vom reduce pana la 0        
                
    def jump(self):
        if self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5

    def dash(self):
        if not self.dashing:
            if self.flip:
                self.dashing = -60 # 60 semnificand aporape 1 secunda
            else:
                self.dashing = 60   
    def render(self, surf, offset=(0, 0)):
        #practic daca fac dash nu randez playerul
        if abs(self.dashing) <= 50:
            super().render(surf, offset = offset) 
           