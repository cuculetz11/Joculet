
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
        self.can_double_jump = False  # control double jump
        self.can_dash = False  # control dash
        self.can_projectile = False  # controloeza proiectilele
        self.attack_cooldown = 0
        self.dark_overlay = False  # Indicator pentru overlay întunecat
        self.display_message = ""  # Mesajul afisat pe ecran
        self.ramen_cool_down = 20  # Cooldown pentru a evita consumul rapid de ramen

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)
        self.attack_cooldown = max(0, self.attack_cooldown - 1)
        self.air_time += 1

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1  # reseteaza jump-urile
            if self.can_double_jump:
                self.jumps = 2  # permite double jump daca a mancat ramen

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
            self.ramen_cool_down -= 1
            
        if self.ramen_cool_down == 0:  
            if self.game.level == 0:
                self.can_double_jump = True  # deblocheaza double jump
                self.jumps = 2  # primeste un jump in plus
            if self.game.level == 1:
                self.can_dash = True
            if self.game.level == 2:
                self.can_projectile = True    
            # incarca urmatorul nivel
            self.game.sfx['new_level'].play()
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
                    "Eat Ramen to unlock a superpower: rassengan (press s to use it)\n"
                    "With rassengan you can kill enemies and progress to the next level."        
                )
            if(self.game.level == 3):
                self.display_message = (
                    "Get ready for the war"
                )
        else:
                self.dark_overlay = False  # dezactivez overlay-ul
                self.display_message = "Cica un info random"

    def check_sasuke(self):
        if self.rect().colliderect(pygame.Rect(int(self.game.sasuke[0]), int(self.game.sasuke[1]), 10, 10)) and self.game.orochimaru == False:
            # Marcheaza jocul ca fiind castigat
            self.game.win = True
            pygame.mixer.music.stop()
        
            # Reda efectul sonor de castig
            self.game.sfx['win'].play()
            # Creeaza un overlay intunecat
            overlay = pygame.Surface(self.game.screen.get_size())  # Creeaza un ecran de aceeasi dimensiune
            overlay.set_alpha(150)  # Seteaza transparenta (0 - complet transparent, 255 - complet opac)
            overlay.fill((0, 0, 0))  # Coloreaza overlay-ul in negru

            # Afiseaza mesajul de castig
            font = pygame.font.Font('data/fonts/naruto.ttf', 45)  # Font personalizat
            text = font.render("You saved Sasuke! You won!", True, (255, 165, 0))  # Portocaliu Naruto

            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                # Deseneaza overlay-ul si mesajul
                self.game.screen.blit(overlay, (0, 0))
                self.game.screen.blit(text, (self.game.screen.get_width() // 2 - text.get_width() // 2,
                                            self.game.screen.get_height() // 2 - text.get_height() // 2))

                pygame.display.flip()  # Actualizeaza ecranul
                pygame.time.wait(7000)  # Asteapta
                running = False  # inchide bucla

            # Opreste jocul
            pygame.quit()
            exit()

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