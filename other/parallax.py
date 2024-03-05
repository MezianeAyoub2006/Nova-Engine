from engine.core.game_object import *

class ParallaxeLayers(GameObject):
    def __init__(self, game, layers):
        self.layers = layers
        super().__init__(game)
    def render(self, scene):
        for depth in self.layers:
            image = self.game.assets[self.layers[depth]]
            image_width = image.get_width()
            x_position = -depth[0] * self.game.camera[0] % image_width
            self.game.background_draw(image, (x_position, 0), depth[1], scene)
            self.game.background_draw(image, (x_position - image_width, 0), depth[1], scene)
            if x_position > 0:
                self.game.background_draw(image, (x_position - image_width, 0), depth[1], scene)
            if x_position - image_width > 0:
                self.game.background_draw(image, (x_position, 0), depth[1], scene)
