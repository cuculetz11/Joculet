import pygame
import random
import math
from scripts.particle import Particle
from scripts.entities import PhysicsEntity

class SmartEnemy(PhysicsEntity):
    """
    Clasa pentru un inamic puternic și inteligent:
    - Urmărește jucătorul în timp real.
    - Poate sări peste obstacole pentru a ajunge la jucător.
    - Trage mai rapid și își ajustează direcția de atac.
    - Este mai agil și mai adaptiv.
    """
    def __init__(self, game, pos, size):
        super().__init__(game, 'smart_enemy', pos, size)
        self.health = 10
        self.attack_cooldown = 0
        self.jump_cooldown = 0
        self.chase_distance = 200  # Distanta maxima la care poate urmari jucatorul
        self.shooting_distance = 150  # Distanta maxima la care poate trage in jucător
        self.speed = 2  # Viteza de deplasare
        self.jump_power = -3  # Puterea sariturii
        self.wait_time = 0  # Timer pentru asteptare in caz de obstacol
        self.walking = 0

    def take_damage(self):
        self.health -= 1

    def update(self, tilemap, movement=(0, 0)):
        if self.health <= 0:
            self.game.sfx['boss_kill'].play()
            self.game.orochimaru = False
            self.game.enemies.remove(self)
            return

        player_dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
        player_distance = math.hypot(player_dis[0], player_dis[1])

        # urmarirea jucătorului
        if player_distance < self.chase_distance and self.wait_time == 0:
            if abs(player_dis[0]) > 10:  # Evitam obstacolele la distanta mica
                movement = ((-self.speed if player_dis[0] < 0 else self.speed), movement[1])

        # Detectarea obstacolelor in fata inamicului
        if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
            if self.collisions['right'] or self.collisions['left']:
                self.flip = not self.flip
            else:
                movement = (-0.5 if self.flip else 0.5, movement[1])
        else:
            self.flip = not self.flip
            self.walking = max(0, self.walking - 1)

        # Salt continuu daca este pe sol si cooldown-ul permite
        if self.collisions['down'] and self.jump_cooldown == 0:
            self.game.sfx['jump'].play()
            self.velocity[1] = self.jump_power
            self.jump_cooldown = 60
        else:
            self.velocity[1] = 0   

        # Reducem cooldown-ul pentru asteptare
        if self.wait_time > 0:
            self.wait_time -= 1

        # Reducem cooldown-ul pentru sarituri
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

        # Daca inamicul nu are cooldown de asteptare, incearca sa traga
        if player_distance < self.shooting_distance and self.wait_time == 0:
            if self.attack_cooldown == 0:
                bullet_speed = 1.5 if player_dis[0] > 0 else -1.5
                self.game.sfx['shoot'].play()
                self.game.projectiles.append([
                    [self.rect().centerx, self.rect().centery],  # Pozitia glontului
                    bullet_speed,  # Directia si viteza
                    0  # Timer
                ])
                self.attack_cooldown = 50  # Cooldown pentru urmatorul atac

        # Reducem cooldown-ul pentru atacuri
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Actualizare pozitie
        super().update(tilemap, movement=movement)

        # Setam animatiile
        if movement[0] != 0:  # Daca se misca
            self.set_action('smart_enemy/run')
        elif self.wait_time > 0:  # Daca asteapta
            self.set_action('smart_enemy/idle') 
        elif not self.collisions['down']:  # Daca sare
            self.set_action('smart_enemy/jump')
        else:  # Daca sta pe loc
            self.set_action('smart_enemy/idle')

        # eliminarea la coliziune cu jucatorul in dash
        if abs(self.game.player.dashing) >= 60:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.sfx['hit'].play()
                self.health -= 2
        else:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.sfx['hit'].play()
                self.game.player.health -= 1
                self.game.player.pos[0] += 30 if self.game.player.flip else -30

                for i in range(20):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 0.5 + 0.5
                    pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                    self.game.particles.append(Particle(self.game, 'shoots', self.game.player.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
