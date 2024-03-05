class GameObject:
    def __init__(self, game, z_pos=0):
        self.game = game
        self.tags = ["@game_object"]
        self.z_pos = z_pos
        self.erased = False

    def kill(self):
        self.erased = True

    def revive(self):
        self.erased = False

    def update(self, scene):
        pass

    def render(self, scene):
        pass

    def __sceneinit__(self, scene):
        pass

    def __endloop__(self, scene):
        pass