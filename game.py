import pygame
import sys
from scripts.enemy import  Enemy
from scripts.player import Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.potato_enemy import PotatoEnemy
from scripts.smart_enemy import SmartEnemy
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
            'background' : load_image('sky.jpg'),
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

            'smart_enemy/idle_animation': Animation(load_images('entities/smart_enemy/idle'), img_dur=7),
            'smart_enemy/run_animation': Animation(load_images('entities/smart_enemy/run'), img_dur=5),
            'smart_enemy/jump_animation': Animation(load_images('entities/smart_enemy/jump')),

            'inima': load_image("inima.png"),
            'ramen': load_image("ramen.png"),
            'rassengan': load_image("projectile_hero.png"),
            'run_animation': Animation(load_images('entities/player/run'), img_dur=5),
            'jump_animation': Animation(load_images('entities/player/jump'))

            
        } #dictionar key:String, value: path la img

        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit1.wav'),
            'ramen': pygame.mixer.Sound('data/sfx/ramen.wav'),
            'info': pygame.mixer.Sound('data/sfx/info.wav'),
            'death': pygame.mixer.Sound('data/sfx/death.wav'),
            'new_level': pygame.mixer.Sound('data/sfx/new_level.wav'),
            'win': pygame.mixer.Sound('data/sfx/win.wav'),
            'boss_kill': pygame.mixer.Sound('data/sfx/boss_kill.wav')
        }

        self.sfx['jump'].set_volume(0.6)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.6)
        self.sfx['ramen'].set_volume(0.7)
        self.sfx['info'].set_volume(0.2)
        self.sfx['death'].set_volume(0.2)
        self.sfx['new_level'].set_volume(0.6)
        self.sfx['win'].set_volume(1)
        
        self.health_hero = 3
        self.player = Player(self, 'player', (50,50), (8, 15))
        self.win = False
        self.tilemap = Tilemap(self,tile_size = 16)
        self.ramen = []
        self.info = []
        self.sasuke = []
        self.orochimaru = True
        self.level = 0
        self.load_level(self.level)
        self.clouds = Clouds(self.assets['clouds'], count=16)

        
    #spawnerul 0 e playerul, iar spawnerul 1 e inamicul(asa le punem in editor)
    def load_level(self, map_id):
        self.tilemap.load('data/levels/' + str(map_id) + '.json')
        self.player.health = 3
        self.enemies = []
        self.player.ramen_cool_down = 20
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1), ('spawners', 2), ('spawners', 3)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            elif spawner['variant'] == 1:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))
            elif spawner['variant'] == 2:
                self.enemies.append(PotatoEnemy(self, spawner['pos'], (8, 15)))
            elif spawner['variant'] == 3:
                self.enemies.append(SmartEnemy(self, spawner['pos'], (8, 15)))    

        self.projectiles = []
        self.hero_projectiles = []
        self.particles = []
        self.scroll = [0, 0]
        for tile in self.tilemap.tilemap.values():
            if tile['type'] == 'decor' and tile['variant'] == 5:
                self.ramen = tile['pos']
            if tile['type'] == 'decor' and tile['variant'] == 4:
                self.info = tile['pos']
        if(self.level == 3):
            for tile in self.tilemap.offgrid_tiles:
                if tile['type'] == 'decor' and tile['variant'] == 6:
                    self.sasuke = tile['pos']
                    break       
        self.transition = -30
    
    def render_overlay(self):
        if self.player.dark_overlay:  # Dacă trebuie să afișăm overlay
            # Creăm un strat întunecat
            dark_surface = pygame.Surface(self.screen.get_size())
            dark_surface.set_alpha(140)  # Transparență
            dark_surface.fill((0, 0, 0))
            self.screen.blit(dark_surface, (0, 0))

            # Font pentru titlu
            title_font = pygame.font.Font(None, 60)  # Font mai mare pentru titlu
            title_text = title_font.render("INFO POINT", True, (255, 69, 0))  # Titlu alb
            title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 90))  # Plasăm titlul sus
            self.screen.blit(title_text, title_rect)  # Desenăm titlul pe ecran

            # Font pentru textul informativ
            font = pygame.font.Font('data/fonts/naruto.ttf', 20)
            lines = self.player.display_message.split('\n')  # Împărțim mesajul în linii
            y_offset = 200  # Poziționare mai jos pentru textul informativ

            for line in lines:
                text = font.render(line, True, (255, 255, 255))  # Text alb
                text_rect = text.get_rect(center=(self.screen.get_width() // 2, y_offset))  # Poziționare pe verticală
                self.screen.blit(text, text_rect)  # Desenăm fiecare linie pe ecran
                y_offset += text.get_height() + 5  # Creștem offset-ul pentru linia următoare


    def run(self):
        #metoda publica
        pygame.mixer.music.load('data/naruto_music.wav')
        pygame.mixer.music.set_volume(0.5)      
        pygame.mixer.music.play(-1)

        while True:
            self.display.blit(self.assets['background'], (0,0)) #destination.blit(source, position)

            if not len(self.enemies): # asta ar fi daca am omori toti enemies, dar vrem dupa ce atinge ramen ul
                self.transition += 1
            if self.transition < 0:
                self.transition += 1

            background_scaled = pygame.transform.scale(self.assets['background'], self.display.get_size())
            self.display.blit(background_scaled, (0, 0))  # Draw the scaled image
            self.scroll[0] += int((self.player.pos[0] - self.scroll[0] - 160) / 8) # -x este pentru o comensare sa fie la jumatatea ecarnului, iar impartirea este pentru a aduga un smooth scroll
            self.scroll[1] += int((self.player.pos[1] - self.scroll[1] - 120) / 8)
            
            self.clouds.update()
            self.clouds.render(self.display, offset = self.scroll)
            
            self.tilemap.render(self.display, offset=self.scroll)
            self.player.check_fall()
            self.player.check_ramen()
            self.player.check_info()
            if(self.level == 3):
                self.player.check_sasuke()
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
                    self.sfx['death'].play()
                    self.load_level(self.level)
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
                        self.sfx['hit'].play()
                        self.projectiles.remove(projectile)
                        self.player.health -= 1
                        #cand il atince un proiectil, ii scadem viata
            

            for hero_projectile in self.hero_projectiles.copy():
                hero_projectile[0][0] += hero_projectile[1]
                hero_projectile[2] += 1
                img = self.assets['rassengan']
                self.display.blit(img, (hero_projectile[0][0] - img.get_width() / 2 - self.scroll[0], hero_projectile[0][1] - img.get_height() / 2 - self.scroll[1]))
                if self.tilemap.solid_check(hero_projectile[0]):
                    self.hero_projectiles.remove(hero_projectile)
                elif hero_projectile[2] > 360:
                    self.hero_projectiles.remove(hero_projectile)
                for enemy in self.enemies.copy():
                    if enemy.rect().collidepoint(hero_projectile[0]):
                        enemy.take_damage()
                        self.sfx['hit'].play()
                        
                        for i in range(20):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 0.5 + 0.5
                            pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                            self.particles.append(Particle(self, 'shoots', enemy.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
                        try:
                            self.hero_projectiles.remove(hero_projectile)
                        except ValueError:
                            pass  #aici avem un bug pe care nu l-am putut rezolva, dar nu afecteaza jocul
                        #se sterge proiectilul inainte ca aceasta functie sa l stearga, de aceea trebuie sa punem un try except



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
                if event.type == pygame.KEYDOWN: #eveniment generat de apasarea unei taste
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        self.player.jump() # saritura
                    if event.key == pygame.K_x and self.player.can_dash:
                        self.player.dash()
                    if event.key == pygame.K_s and self.player.can_projectile:
                        self.player.attack()
                    # if event.key == pygame.K_t:  #mapa pentru testare
                    #     self.player.can_dash = True
                    #     self.player.can_projectile = True
                    #     self.player.can_double_jump = True
                    #     self.level = 4
                    #     self.load_level(4)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:#evenimet generat de ridicarea unei taste
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False        
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            self.render_overlay()
            pygame.display.update()

            self.clock.tick(70) #dynamic sleep

Game().run() #instantiem clasa si apelam metoda run