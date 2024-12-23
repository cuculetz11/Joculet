import pygame
import json


AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
} #cum nu puteam folosi o lista pentru o cheie de dictionar am folosit un tuple

NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]

PHYSICS_TILES = {'grass', 'stone'} # acesta e un set ce contine tipurile de tileuri ce vor avea coliiziuni O(1)

AUTOTILE_TYPES = {'grass', 'stone'}


class Tilemap:
    #tile_size ul reperzinta dimenisuea unei placi de tiles cum ar fi aici e 16x16
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} #dictionar in vare salvam pozitia in acest stil "1;10" si ce avem la aceea pozitie e un tile ce are campurile 'type','variant', 'pos' 
        self.offgrid_tiles = [] #lista cu elemente ce nu respecta gridul, adica nu sunt pe o placa de tiles le pot pune cum vreau eu (suprapuse sau cum vreau)

    def extract(self, id_pairs, keep=False):
        matches = []
        # Use a copy of the keys of the dictionary to avoid modifying while iterating
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in list(self.tilemap.keys()):  # Use list() to get a copy of the keys
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]

        return matches


                

    def tiles_around(self, pos):
        """
        Aceasta functie verifica daca exista tileuri in jurul unei pozitii date, practic pentru a realiza coliiziuni

        Args: pozitia pentru care vrem sa verificam daca exista tileuri in jur
        Returneaza: o lista de tileuri in jurul pozitiei date
        """
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)) # folosind int (x//y) obtinem fix partea intreaga a numarului x/y
        tiles = []
        for offset in NEIGHBOR_OFFSET:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1]) # practic obtinem 9 pozitii
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def solid_check(self, pos):
        """
        Aceasta functie verifica daca o pozitie este pe un tile solid
        """
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]


    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()

    def autotile(self):
        """
        Parcurege fiecare tile din mao si verifica vecinii, daca cumva sunt la fel cauta un tile cat mai potivit
        """
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]

    def physics_around(self,pos):
        recs = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                recs.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size)) #creem un dreptunghi pentru a realiza coliiziuni
        return recs
    def get_tile_at(self, pos):
        """
        retunreaza tipul tile-ului de la o anumita pozitie
        """
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            return self.tilemap[tile_loc]['type']
        return None

    def render(self,surf, offset = (0,0)):
        
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']] , (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1])) #acelasi lucru ca mai jos doar ca aici nu tinem connt de dimensiunea unu tile
            
        # cauta toate tile-urile din dictionar si le randeaza pe ecran, toate tileurile fiind incarcate in game.assets
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0]  * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1])) # acel offset e pentru a putea face scroll pe harta imitand o camera
