import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) #e mai usor de lucrat cu liste
        self.size = size
        self.velocity = [0, 0] # viteza derivivata pozitiei
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

    def rect(self):
        """
        Face un dreptunghi ce reprezinta aceasta entitate pemtru a putea realiza apoi coliziuni
        Args: self- ce repezinta intanta acestei clase( diferenta fata de java )
        Returneaza: un dreptunghi ce reprezinta aceasta entitate
        """
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0] #miscarea pe axa x

        entity_rect = self.rect()

        for react in tilemap.physics_around(self.pos):
            if entity_rect.colliderect(react):
                if frame_movement[0] > 0:
                    entity_rect.right = react.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = react.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x # setam pozitia pe x astfel incat se azugura ca nu poate trece prin tile              

        self.pos[1] += frame_movement[1] #miscarea pe axa y
        entity_rect = self.rect()
        for react in tilemap.physics_around(self.pos):
            if entity_rect.colliderect(react):
                if frame_movement[1] > 0:
                    entity_rect.bottom = react.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = react.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y


        self.velocity[1] = min(9, self.velocity[1] + 0.2)  #g ravitatie 9 reprezentand valoarea maxima a vitezei, celalata  0.1 reprezentand acceleratia
    
        if(self.collisions['down'] or self.collisions['up']):
            self.velocity[1] = 0 # resetam viteza pe axa y in momentul in care avem o coliziune
            
    def render(self, surf, offset=(0, 0)):
        surf.blit(self.game.assets['player'], (self.pos[0]- offset[0], self.pos[1] - offset[1]))