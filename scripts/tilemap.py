import pygame

NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]

PHYSICS_TILES = {'grass', 'stone'} #acesta e un set ce contine tipurile de tileuri ce vor avea coliiziuni O(1)


class Tilemap:
    #tile_size ul reperzinta dimenisuea unei placi de tiles cum ar fi aici e 16x16
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} #dictionar in vare salvam pozitia in acest stil "1;10" si ce avem la aceea pozitie e un tile ce are campurile de mai jos 'type','variant', 'pos' 
        self.offgrid_tiles = [] #lista elemente 

        for i in range(200):
            self.tilemap[str(3 + i) + ';10'] = {'type' : 'grass', 'variant' : 1, 'pos' : (3 + i, 10)} #ne miscampe linie #variant este indexul imaginii din lista de imagini

        for i in range(13):    
            self.tilemap['10;' + str(i + 5)] = {'type': 'stone', 'variant' : 1, 'pos' : (10, i + 5)} #ne miscam pe coloana
            for i in range(5):
                self.tilemap[str(5 + i) + ';' + str(10 - i)] = {'type': 'stone', 'variant': 1, 'pos': (5 + i, 10 - i)} # rampa diagonala


    def tiles_around(self, pos):
        """
        Aceasta functie verifica daca exista tileuri in jurul unei pozitii date, practic pentru a realiza coliiziuni

        Args: pozitia pentru care vrem sa verificam daca exista tileuri in jur
        Returneaza: o lista de tileuri in jurul pozitiei date
        """
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)) #folositd int (x//y) obtinem fix partea intreaga a numarului x/y
        tiles = []
        for offset in NEIGHBOR_OFFSET:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1]) #practic obtinem 9 pozitii
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_around(self,pos):
        recs = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                recs.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size)) #creem un dreptunghi pentru a realiza coliiziuni
        return recs
    
    def render(self,surf, offset = (0,0)):

        for tile in self.offgrid_tiles:
            pass

        # cauta toate tile-urile din dictionar si le randeaza pe ecran, toate tileurile fiind incarcate in game.assets
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            img = self.game.assets[tile['type']][tile['variant']]
            surf.blit(img, (tile['pos'][0]  * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1])) # acel offset e pentru a putea face scroll pe harta imitand o camera
