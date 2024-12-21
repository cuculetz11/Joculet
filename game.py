import pygame
import sys
from scripts.enemy import  Enemy
from scripts.player import Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.potato_enemy import PotatoEnemy
import math
import random
from scripts.particle import Particle

class Game:
    def __init__(self):
        #metoda privata

        pygame.init()

        pygame.display.set_caption('First Game')
        self.screen = pygame.display.set_mode((1024, 768))

        self.display = pygame.Surface((320,240))

        self.clock = pygame.time.Clock()
  
        self.movement = [False, False] #mers stanga, dreapta

        self.assets = {
            'player': load_image('entities/player.png'), #resursele jocului asta i playerul
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'stone' : load_images('tiles/stone'),
            'large_decor' : load_images('tiles/large_decor'),
            'background' : load_image('background.png'),
            'clouds' : load_images('clouds'),
            'idle_animation': Animation(load_images('entities/player/idle'), img_dur=7),
            'run_animation': Animation(load_images('entities/player/run'), img_dur=5),
            'jump_animation': Animation(load_images('entities/player/jump')),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'particle/shoots' : Animation(load_images('particles/shoots'), img_dur=6, loop=False),
            'enemy/idle_animation': Animation(load_images('entities/enemy/idle'), img_dur=7),
            'enemy/run_animation': Animation(load_images('entities/enemy/run'), img_dur=5),
            'potato_enemy/idle_animation': Animation(load_images('entities/potato_enemy/idle'), img_dur=7),
            'potato_enemy/run_animation': Animation(load_images('entities/potato_enemy/run'), img_dur=5),

            'kunai': load_image("kunai.png"),
            'shuriken': load_image("projectile.png"),

            'inima': load_image("inima.png"),
        } #dictionar key:String, value: path la img
        
        self.health_hero = 3
        self.player = Player(self, 'player', (50,50), (8, 15))
        
        self.tilemap = Tilemap(self,tile_size = 16)
    
        self.load_level(3)
        self.clouds = Clouds(self.assets['clouds'], count=16)

    

        #spawnerul 0 e playerul, iar spawnerul 1 e inamicul(asa le punem in editor)
     

    def load_level(self, map_id):
        self.tilemap.load('data/levels/' + str(map_id) + '.json')
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1), ('spawners', 2)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            elif spawner['variant'] == 1:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))
            elif spawner['variant'] == 2:
                self.enemies.append(PotatoEnemy(self, spawner['pos'], (8, 15)))

        
        self.projectiles = []
        self.particles = []
        self.scroll = [0, 0]

    def run(self):
        #metoda publica
        while True:
            self.display.blit(self.assets['background'], (0,0)) #destination.blit(source, position)
            
            self.scroll[0] += int((self.player.pos[0] - self.scroll[0] - 160) / 8) # -x este pentru o comensare sa fie la jumatatea ecarnului, iar impartirea este pentru a aduga un smooth scroll
            self.scroll[1] += int((self.player.pos[1] - self.scroll[1] - 120) / 8)
            
            self.clouds.update()
            self.clouds.render(self.display, offset = self.scroll)
            
            self.tilemap.render(self.display, offset=self.scroll)
            self.player.check_fall()
            # randam enemies
            for enemy in self.enemies.copy():
                enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=self.scroll)

            if self.player.health > 0:
                a = 6
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset = self.scroll) 
            else:
                a = a - 1
                if a == 0:
                    self.load_level(3)
                    self.player.health = 3

            for i in range(self.player.health):#pentru afisarea vietii eroului
                self.display.blit(self.assets['inima'], (self.display.get_width() - 20 * (i + 1), 10))

            # [(x,y), directie, timer] pentru fiecare proiectil
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1] #adunam directia la x
                projectile[2] += 1 # marim timer ul
                img = self.assets['shuriken']

                # afisam proiectilele
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - self.scroll[0], projectile[0][1] - img.get_height() / 2 - self.scroll[1]))
                
                # facem sa dispara proiectilele daca lovesc ceva
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                elif projectile[2] > 420: # verificam sa nu stea proiectilele la infinit pe ecran (in caz ca nu lovesc nimic si raman pe harta (6 secunde))
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 60: # daca player-ul e in dash, nu moare
                    if self.player.rect().collidepoint(projectile[0]):
                        for i in range(20):
                            #exact acelasi lucru ca la dash numai ca am schimbat culoarea particulelor
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 0.5 + 0.5
                            pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                            self.particles.append(Particle(self, 'shoots', self.player.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
                        self.projectiles.remove(projectile)
                        self.player.health -= 1
                        #cand il atince un proiectil, ii scadem viata

            # la fiecare frame noi randam particulele pentru dash si le stegem dupa ce si au terminat animatia 
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset = self.scroll)
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get(): # ia inputul oricare ar fi el
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                if event.type == pygame.KEYDOWN: #evenimet generat de apasarea unei taste
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        self.player.jump() # saritura
                    if event.key == pygame.K_x:
                        self.player.dash()              
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:#evenimet generat de ridicarea unei taste
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False        
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))

            pygame.display.update()

            self.clock.tick(70) #dynamic sleep

Game().run() #instantiem clasa si apelam metoda run