
import random
import math
import pygame
from scripts.entities import PhysicsEntity
from scripts.particle import Particle

class Player(PhysicsEntity):
    """
    dash ul ia cate 2 din viata enemy-ului
    iar aruncatu cu proiectile ii ia 1 viata enemy-ului
    """
    def __init__(self, game, e_type, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0  # timpul in aer pentru a sti cand sa afisam animatia de saritura
        self.jumps = 1
        self.dashing = 0
        self.health = 3
        self.can_double_jump = False  # New flag to control double jump
        self.can_dash = False  # New flag to control dash
        self.can_projectile = False  # New flag to control projectile
        self.attack_cooldown = 0
        self.dark_overlay = False  # Indicator pentru overlay întunecat
        self.display_message = ""  # Mesajul afișat pe ecran
        
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)
        self.attack_cooldown = max(0, self.attack_cooldown - 1)
        self.air_time += 1

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1  # Reset to 1 jump by default
            if self.can_double_jump:
                self.jumps = 2  # Allow double jump only if unlocked

        if self.air_time > 4:
            self.set_action('jump')    
        elif movement[0] != 0:
            self.set_action('run')    
        else:
            self.set_action('idle')

        if abs(self.dashing) in {70, 60}:
            for i in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))

        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)

        if abs(self.dashing) > 60:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 61:
                self.velocity[0] *= 0.1
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))

        if self.velocity[0] > 0:
            self.velocity[0] = max(0, self.velocity[0] - 0.1)
        else:
            self.velocity[0] = min(0, self.velocity[0] + 0.1)

    def check_fall(self):
        if self.pos[1] > 350:
            self.game.sfx['death'].play()
            self.health = 0
            self.game.load_level(self.game.level)
            self.game.player.health = 3

    def attack(self):
        if self.attack_cooldown == 0:
            self.game.sfx['shoot'].play()
            if self.flip:
                self.game.hero_projectiles.append([[self.rect().centerx - 7, self.rect().centery], -3, 0])
            else:
                self.game.hero_projectiles.append([[self.rect().centerx + 7, self.rect().centery], 3, 0])
            self.attack_cooldown = 45

    def check_ramen(self):
        if self.rect().colliderect(pygame.Rect(int(self.game.ramen[0]) * 16, int(self.game.ramen[1]) * 16, 10, 10)):
            self.game.sfx['ramen'].play()
            if self.game.level == 0:
                self.game.sfx['new_level'].play()
                self.can_double_jump = True  # Unlock double jump
                self.jumps = 2  # Grant double jump immediately
            if self.game.level == 1:
                self.game.sfx['new_level'].play()
                self.can_dash = True
            if self.game.level == 2:
                self.game.sfx['new_level'].play()
                self.can_projectile = True    
            # Load the next level
            self.game.level += 1
            self.game.load_level(self.game.level)

    def check_info(self):
        if self.rect().colliderect(pygame.Rect(int(self.game.info[0]) * 16, int(self.game.info[1]) * 16, 10, 10)):
            self.game.sfx['info'].play()
            self.dark_overlay = True  # va face ecranul sa se intunece cand ating info
            if(self.game.level == 0):
                self.display_message = (
                    "Naruto is searching for Sasuke to bring him back to the village\n"
                    "He has lost his powers and needs to regain them.\n"
                    "Eat Ramen to unlock a superpower: double jump \n"
                    "and progress to the next level."
                )
            if(self.game.level == 1):
                self.display_message = (
                    "Eat Ramen to unlock a superpower: dash (press x to use it)\n"
                    "With dash you can kill enemies and progress to the next level."
                )
            if(self.game.level == 2):
                self.display_message = (
                    "Eat Ramen to unlock a superpower: rassengan (press z to use it)\n"
                    "With rassengan you can kill enemies and progress to the next level."        
                )
            if(self.game.level == 3):
                self.display_message = (
                    "Get ready for the war"
                )
        else:
                self.dark_overlay = False  # dezactivez overlay-ul
                self.display_message = ""

    # def check_sasuke(self):
    #     print(self.game.sasuke[0], self.game.sasuke[1])
    #     # if self.rect().colliderect(pygame.Rect(int(self.game.sasuke[0]) * 16, int(self.game.sasuke[1]) * 16, 10, 10)):
    #     #     self.game.win = True
    #     #     print("You saved Sasuke! You win!")
    def jump(self):
        if self.jumps > 0:
            self.game.sfx['jump'].play()
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5

    def dash(self):
        
        if not self.dashing:
            self.game.sfx['dash'].play()
            if self.flip:
                self.dashing = -70
            else:
                self.dashing = 70  

    def render(self, surf, offset=(0, 0)):
        if abs(self.dashing) <= 60:
            super().render(surf, offset=offset)