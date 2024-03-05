z_pos_func = lambda obj : obj.z_pos
from engine.context.context import *

class Scene:
    def __init__(self, game:GameContext):
        self.objects = []
        self.iter = 0
        self.game = game

    def update(self):
        if self.iter == 0:
            for object in sorted(self.objects, key=z_pos_func):
                object.__sceneinit__(self)
            self.iter = 1
        for object in sorted(self.objects, key=z_pos_func):
            if not self.game.freeze:
                object.update(self)
            object.render(self)
            object.__endloop__(self)
        self.objects = list(filter(lambda x : not x.erased, self.objects))
    
    def link(self, *args):
        for arg in args:
            self.objects.append(arg)
    
    def get_objects(self) -> list:
        return self.objects

    def get_objects_by_tags(self, *tags) -> list:
        objs = []
        for obj in self.objects:
            if set(tags).intersection(set(obj.tags)):
                objs.append(obj)
        return objs
    
    def get_objects_by_tag(self, tag) -> list:
        return list(filter(lambda obj : tag in obj.tags, self.objects))
