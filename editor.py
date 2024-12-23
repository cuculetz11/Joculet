import pygame
import sys
from scripts.utils import load_image,load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 768 / 240
#3.2 
class Game:
    """
    Acesta clasa este pentru editor ce are urmatoarele functionalitati
    - click stanga pune un block pe pozitia cursorului
    - click dreapta sterge un block de pe pozitia cursorului
    - lShift poti sa schimbi varianta tileului
    - din WASD miscam camera
    - lCtrl pentru a schimba intre grid si offgrid adica poti pune chestii fara sa respecti distanta de 16x16
    - o pentru a salva harta
    - t pentru a face autotile(adica poti folosi doar un tip de tile si apasand t o sa arate harta 'mai bine')
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
            'spawners': load_images('tiles/spawners'),
        } #dictionar key:String, value: path la img
          
        self.movement = [False, False, False, False] # move camera up, down, left, right
        
        self.tilemap = Tilemap(self,tile_size = 16)

        self.scroll = [0,0]
    
        self.tile_list = list(self.assets)
        self.tile_group = 0 # indexul tileului din lista
        self.tile_variant = 0

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass


        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

    def run(self):
        # metoda publica
        while True:
            self.display.fill((0,0,0)) # destination.blit(source, position)
            
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2 #miscarea camerei pe axa x
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2 #miscarea camerei pe axa y
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset = render_scroll) #pentru a randa/desena tilemapul(ce preprezinta harta)
            curr_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            curr_tile_img.set_alpha(128)


            mpos = pygame.mouse.get_pos() # coordonatele mouse-ului
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))
            
            if self.ongrid:
                self.display.blit(curr_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(curr_tile_img, mpos)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos} #adaugam un tile in tilemap ce se afpla pe grid

          
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc] # stergem un tile din tilemap
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile) # stergem un tile din lista de tileuri ce nu sunt pe grid


            self.display.blit(curr_tile_img, (5,5))
            
            for event in pygame.event.get(): # ia inputul oricare ar fi el
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:     # click stanga
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])}) #aduga in lista de elemenete ce nu sunt pe grid
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:    
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]]) # dam scroll prin tileuri
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list) # dam scroll prin tileuri
                        if event.button == 5:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                        self.tile_variant = 0 # il facem 0 ca altfel ar fi dat out of range daca cumva ne duceam la un tile cu mai multe variante si ramaneam la un index mare si apor reveneam la un tile ce are mai putine variante

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN: # eveniment generat de apasarea unei taste
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True    
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()    
                    if event.key == pygame.K_LSHIFT:
                        if self.shift:
                            self.shift = False
                        else:
                            self.shift = True
                    if event.key == pygame.K_LCTRL:
                        if self.ongrid:
                            self.ongrid = False
                        else:
                            self.ongrid = True
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a: #eveniment generat de ridicarea unei taste
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))

            pygame.display.update()

            self.clock.tick(70) # dynamic sleep

Game().run() # instantiem clasa si apelam metoda run