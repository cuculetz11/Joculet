class Particle:
    """
    Este o clasa pentru particule, acestea sunt folosite pentru a crea efecte vizuale

    Args: game - instanta curenta a jocului
          p_type - tipul particulei
          pos - pozitia la care se va afisa particula
          velocity - viteza particulei
          frame - frame-ul de la care incepe animatia      
    """    
    def __init__(self, game, p_type, pos, velocity=[0, 0], frame=0):
        self.game = game
        self.type = p_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.animation = self.game.assets['particle/' + p_type].copy()
        self.animation.frame = frame
    
    def update(self):
        """
        Dupa ce particula si a terminat animatia, aceasta va fi eliminata
        """
        kill = False
        if self.animation.done:
            kill = True
        
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        
        #folosit pentru deplasarea particulelor
        
        self.animation.update()
        
        #in caz ca vreum sa eliminam particulele ne folosiim de kill  
        return kill
    
    def render(self, surf, offset=(0, 0)):
        img = self.animation.img()
        surf.blit(img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))
    