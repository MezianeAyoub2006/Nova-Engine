from engine.core.game_object import *
from engine.other.utils import generate_screen_positions
from engine.tilemap.tilemap_error import *
import pygame

class Tilemap(GameObject):
    
    def __init__(self, game, tile_size, z_pos, offset=(0, 0)):
        self.tile_size = tile_size
        GameObject.__init__(self, game, z_pos)
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255), (127, 127, 127), (255, 150, 150), (150, 255, 150), (150, 150, 255), (255, 255, 150), (255, 150, 255), (150, 255, 255)]
        self.tilemap = {}
        self.neighboor_offsets = [(i, j) for i in range(-1, 2, 1) for j in range(-1, 2, 1)] + [(0, 0)]
        self.neighboor_offsets.remove((0, 0))
        self.tileset = []
        self.offset = offset
        self.tiles_data = [] 
        self.content = []
        self.animations = {}
        self.tags.append("@tilemap")

    def place_tile(self, id, location, rotation=0, flip_x=False, flip_y=False):
        if id==None:
            return
        try:
            self.tilemap[(location[0]+self.offset[0], location[1]+self.offset[1])] = {"pos" : [self.tile_size*location[0] + self.tile_size*self.offset[0], self.tile_size*location[1] + self.tile_size*self.offset[1]], "id":id, "rotation":rotation, "flip_x":flip_x, "flip_y":flip_y}
        except KeyError:
            raise TilemapError("Missing Tile", location)
        
    def place_pattern(self, pattern, location, rotation=0, flip_x=False, flip_y=False):
        steps = (len(pattern[0]), len(pattern))
        for x in range(steps[0]):
            for y in range(steps[1]):
                try:
                    self.place_tile(pattern[y][x], (location[0]+x, location[1]+y), rotation, flip_x, flip_y)
                except TilemapError:
                    raise
        
    def get_surface_from_location(self, loc):
        tile = self.tilemap[loc]
        if tile != None:
            if tile["id"] in self.animations:
                try:

                    surface = self.tileset[self.animations[tile["id"]][0][int(self.animations[tile["id"]][2])]]
                except:
                    surface = self.tileset[self.animations[tile["id"]][0][0]]
            else:
                surface = self.tileset[tile["id"]] 
        return surface
        
    def render(self, scene):
        if not "#invisible" in self.tags:
            for tile in self.animations:
                if self.animations[tile][2] < len(self.animations[tile][0]) - 1:
                    self.animations[tile][2] += self.animations[tile][1] * self.game.get_dt()
                else:
                    self.animations[tile][2] = 0
            for loc in generate_screen_positions(self.tile_size, self.game.camera, self.game.get_display_size(), self.game.rendering_offset): 
                try:
                    tile = self.tilemap[loc]
                    if tile != None:
                        if tile["id"] in self.animations:
                            try:
                                surface = self.tileset[self.animations[tile["id"]][0][int(self.animations[tile["id"]][2])]]
                            except:
                                surface = surface = self.tileset[self.animations[tile["id"]][0][0]]
                        else:
                            surface = self.tileset[tile["id"]] 
                        if tile["rotation"] != 0:
                            surface = pygame.transform.rotate(surface, tile["rotation"])
                        if tile["flip_x"] or tile["flip_y"]:
                            surface = pygame.transform.flip(surface, tile["flip_x"], tile["flip_y"])
                        self.game.render(surface, tile["pos"])
                    else:
                        del self.tilemap[loc]
                except KeyError:
                    pass
    
    def get_tiles_around(self, pos):
        check_pos = (int(pos[0]) // self.tile_size, int(pos[1]) // self.tile_size)
        tiles = []
        for offset in self.neighboor_offsets:
            pos = (check_pos[0] + offset[0], check_pos[1]+offset[1])
            if pos in self.tilemap:
                tiles.append((pygame.Rect(pos[0]*self.tile_size, pos[1]*self.tile_size, self.tile_size, self.tile_size), self.tilemap[pos]["id"], self.tiles_data[self.tilemap[pos]["id"]]))

        return tiles

    def set_animation_tile(self, id, speed, tiles):
        self.animations[id] = [tiles, speed, 0]

