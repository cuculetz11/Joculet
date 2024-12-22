import pygame
import random
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

        self.attack_cooldown = 0
        self.jump_cooldown = 0
        self.chase_distance = 200  # Distanța maximă la care urmărește jucătorul
        self.shooting_distance = 150  # Distanța maximă la care poate trage în jucător
        self.speed = 2 # Viteza de deplasare
        self.jump_power = -3  # Puterea săriturii

    def update(self, tilemap, movement=(0, 0)):
        player_dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
        player_distance = (player_dis[0] ** 2 + player_dis[1] ** 2) ** 0.5

        # Urmărirea jucătorului
        if player_distance < self.chase_distance:
            if abs(player_dis[0]) > 10:  # Evităm oscilațiile la distanțe mici
                movement = ((-self.speed if player_dis[0] < 0 else self.speed), movement[1])

            # Detectarea unui obstacol specific în față
           # Detectarea obstacolelor în fața inamicului (blocuri 1 sau 2)
        check_x = self.rect().centerx + (-10 if self.flip else 10)  # Punctul din fața inamicului
        check_y_base = self.pos[1] + self.size[1]  # Punctul de la baza inamicului
        check_y_top = check_y_base - 16  # Punctul de deasupra bazei (pentru al doilea bloc)

        # Verificăm dacă este un obstacol în față
        obstacle_base_tile = tilemap.get_tile_at((check_x, check_y_base))
        obstacle_top_tile = tilemap.get_tile_at((check_x, check_y_top))

        # Condiția de săritură: există un obstacol jos sau obstacole pe două nivele
        if (obstacle_base_tile in ['stone', 'grass'] or obstacle_top_tile in ['stone', 'grass']) \
                and self.collisions['down'] and self.jump_cooldown == 0:
            self.velocity[1] = self.jump_power
            self.jump_cooldown = 30  # Resetăm cooldown-ul pentru sărituri


        # Reducem cooldown-ul pentru sărituri
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

        # Tragerea către jucător
        if player_distance < self.shooting_distance:
            if self.attack_cooldown == 0:
                bullet_speed = 4 if player_dis[0] > 0 else -4
                self.game.projectiles.append([
                    [self.rect().centerx, self.rect().centery],  # Poziția glonțului
                    bullet_speed,  # Direcția și viteza
                    0  # Timer
                ])
                self.attack_cooldown = 20  # Cooldown pentru următorul atac

        # Reducem cooldown-ul pentru atacuri
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Actualizare poziție
        super().update(tilemap, movement=movement)

        # Setăm animațiile
        if movement[0] != 0:
            self.set_action('smart_enemy/run')
        elif not self.collisions['down']:
            self.set_action('smart_enemy/jump')
        else:
            self.set_action('smart_enemy/idle')

        # Eliminarea la coliziunea cu jucătorul în dash
        if abs(self.game.player.dashing) >= 60:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.enemies.remove(self)

def render(self, surf, offset=(0, 0)):
    super().render(surf, offset=offset)

    # Desenează o săgeată indicând direcția de urmărire (pentru debugging)
    pygame.draw.line(
        surf, (255, 0, 0),
        (self.rect().centerx - offset[0], self.rect().centery - offset[1]),
        (self.game.player.rect().centerx - offset[0], self.game.player.rect().centery - offset[1]),
        1
    )

