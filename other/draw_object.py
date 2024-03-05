from engine.core.game_object import *
import math

class RenderObject(GameObject):
    def __init__(self, game, image, pos, z_pos):
        GameObject.__init__(self, game, z_pos)
        self.image = image
        self.pos = pos
        self.kill()
    def render(self, scene):
        self.game.render(self.image, (math.floor(self.pos[0]), math.floor(self.pos[1])))
    
class DrawObject(GameObject):
    def __init__(self, game, image, pos, z_pos):
        GameObject.__init__(self, game, z_pos)
        self.image = image
        self.pos = pos
        self.kill()
    def render(self, scene):
        self.game.draw(self.image, (math.floor(self.pos[0]), math.floor(self.pos[1])))

class BackgroundDrawObject(GameObject):
    def __init__(self, game, image, pos, z_pos):
        GameObject.__init__(self, game, z_pos)
        self.image = image
        self.pos = pos
        self.kill()
    def render(self, scene):
        self.game.background_draw(self.image, (math.floor(self.pos[0]), math.floor(self.pos[1])))
    
    