import pygame
import sys
from scripts.utils import load_image,load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 3.2
class Game:
    """
    Acesta clasa este pentru editor ce are urmatoarele functionalitati
    - click stanga pune un block pe pozitia cursorului
    - click dreapta sterge un block de pe pozitia cursorului
    - lShift potisa schimbi varianta tileului
    """
    def __init__(self):
        #metoda privata

        pygame.init()

        pygame.display.set_caption('editor')
        self.screen = pygame.display.set_mode((1024, 768))

        self.display = pygame.Surface((320,240))

        self.clock = pygame.time.Clock()


        self.assets = {
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'stone' : load_images('tiles/stone'),
            'large_decor' : load_images('tiles/large_decor'),

        } #dictionar key:String, value: path la img
          
        self.movement = [False, False, False, False] #move camera up, down, left, right
        
        self.tilemap = Tilemap(self,tile_size = 16)

        self.scroll = [0,0]
    
        self.tile_list = list(self.assets)
        self.tile_group = 0 #indexul tileului din lista
        self.tile_variant = 0
        self.clicking = False
        self.right_clicking = False
        self.shift = False
    def run(self):
        #metoda publica
        while True:
            self.display.fill((0,0,0)) #destination.blit(source, position)

            render_scroll = (int(self.scroll[0]), int(self.scroll[1] ))

            self.tilemap.render(self.display, offset = render_scroll) #pentru a randa/desena tilemapul(ce preprezinta harta)
            curr_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            curr_tile_img.set_alpha(128)


            mpos = pygame.mouse.get_pos() #coordonatele mouseului
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))
            
            if self.clicking:
               self.tilemap.tilemap[str(tile_pos[1]) + ',' + str(tile_pos[0])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos } #adaugam tileul in tilemap
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc] #stergem tileul din tilemap
            self.display.blit(curr_tile_img, (5,5))
            for event in pygame.event.get(): # ia inputul oricare ar fi el
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:     #click stanga
                        self.clicking = True
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:    
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]]) #dam scroll prin tileuri
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list) #dam scroll prin tileuri
                        if event.button == 5:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                        self.tile_variant = 0 #il facem 0 ca altfel ar fi dat out of range daca cumva ne duceam la un tile cu mai multe variante si ramaneam la un index mare si apor reveneam la un tile ce are mai putine variante

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN: #evenimet generat de apasarea unei taste
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True    
                    if event.key == pygame.K_LSHIFT:
                        if self.shift:
                            self.shift = False
                        else:
                            self.shift = True
                    

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:#evenimet generat de ridicarea unei taste
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))

            pygame.display.update()

            self.clock.tick(70) #dynamic sleep

Game().run() #instantiem clasa si apelam metoda run