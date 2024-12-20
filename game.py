import pygame
import sys
from scripts.entities import PhysicsEntity,Player
from scripts.utils import load_image,load_images,Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

class Game:
    def __init__(self):
        #metoda privata

        pygame.init()

        pygame.display.set_caption('First Game')
        self.screen = pygame.display.set_mode((1024, 768))

        self.display = pygame.Surface((320,240))

        self.clock = pygame.time.Clock()
  
        self.movement = [False, False] #mers in sus si in jos

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
            'jump_animation': Animation(load_images('entities/player/jump'))


            
        } #dictionar key:String, value: path la img
        

        self.player = Player(self, 'player', (50,50), (8, 15))
        
        self.tilemap = Tilemap(self,tile_size = 16)

        self.scroll = [0,0]
        
        self.clouds = Clouds(self.assets['clouds'], count=16)

    def run(self):
        #metoda publica
        while True:
            self.display.blit(self.assets['background'], (0,0)) #destination.blit(source, position)
            
            self.scroll[0] += int((self.player.pos[0] - self.scroll[0] - 160) / 8) # -x este pentruo comensare sa fie la jumatatea ecarnului, iar impartirea este penntru a aduga un smooth scroll
            self.scroll[1] += int((self.player.pos[1] - self.scroll[1] - 120) / 8)

            self.clouds.update()
            self.clouds.render(self.display, offset = self.scroll)
            
            self.tilemap.render(self.display, offset = self.scroll) #pentru a randa/desena tilemapul(ce preprezinta harta)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset = self.scroll) 


            for event in pygame.event.get(): # ia inputul oricare ar fi el
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                if event.type == pygame.KEYDOWN: #evenimet generat de apasarea unei taste
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3  # saritura          
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:#evenimet generat de ridicarea unei taste
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False        
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))

            pygame.display.update()

            self.clock.tick(70) #dynamic sleep

Game().run() #instantiem clasa si apelam metoda run