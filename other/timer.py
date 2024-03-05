class Timer:
    def __init__(self, game):
        self.fields = {}
        self.game = game
    def update(self):
        for field in self.fields:
            if self.fields[field] > 0:
                self.fields[field] -= self.game.get_dt()/60
            if self.fields[field] < 0:
                self.fields[field] = 0
    def __setitem__(self, item, value):
        self.fields[item] = value
    def __getitem__(self, field):
        if not field in self.fields:
            self.fields[field] = 0
        return self.fields[field]