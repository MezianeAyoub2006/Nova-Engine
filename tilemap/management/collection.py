from engine.tilemap.tilemap_error import *
from engine.tilemap.tilemap import *

class TilemapCollection:
    def __init__(self, game, tile_size):
        self.tilemaps = {}
        self.game = game
        self.tile_size = tile_size

    def add_tilemaps(self, *tilemaps):
        for tilemap in tilemaps:
            self.tilemaps[tilemap.z_pos] = tilemap

    def link(self, scene):
        for tilemap in self.tilemaps:
            scene.link(self.tilemaps[tilemap])
    
    def __getitem__(self, item):
        return self.tilemaps[item]

    def place_tile(self, id, location, z_pos, rotation=0, flip_x=False, flip_y=False):
        try:
            self.tilemaps[z_pos].place_tile(id, location, rotation, flip_x, flip_y)
        except KeyError:
            raise TilemapError("Missing Tile", location)
        
    def place_pattern(self, pattern, location, z_pos, rotation=0, flip_x=False, flip_y=False):
        self.tilemaps[z_pos].place_pattern(pattern, location, rotation, flip_x, flip_y)
    
    def place_multidim_pattern(self, pattern, location, z_pos, step=1, rotation=0, flip_x=False, flip_y=False, tags={}):
        for i in range(z_pos, len(pattern)+z_pos, step):
            if not i in self.tilemaps.keys():
                self.tilemaps[i] = Tilemap(self.game, self.tile_size, i)
                self.tilemaps[i].tileset = self.tilemaps[0].tileset
                if i in tags:
                    for tag in tags[i]:
                        self.tilemaps[i].tags.append(tag)
            self.tilemaps[i].place_pattern(pattern.data[i-z_pos], location, rotation, flip_x, flip_y)
    
    def get_tiles(self, location):
        tiles = []
        for tilemap in self.tilemaps.values():
            try:
                tiles.append((tilemap.tilemap[location], tilemap.tags, tilemap.z_pos))
            except KeyError:
                pass
        return tiles

    def get_solid_map(self, begin_pos, end_pos):
        start_x, end_x = min(begin_pos[0], end_pos[0]), max(begin_pos[0], end_pos[0])
        start_y, end_y = min(begin_pos[1], end_pos[1]), max(begin_pos[1], end_pos[1])
        matrix = []
        for y in range(start_y, end_y + 1):
            row = []
            for x in range(start_x, end_x + 1):
                tiles = self.get_tiles((x, y))
                row.append(int(any("#solid" in tile[1] for tile in tiles)))
            matrix.append(row)
        return matrix


