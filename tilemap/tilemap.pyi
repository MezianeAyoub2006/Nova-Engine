from engine.core.game_object import *
from engine.other.utils import generate_screen_positions
from engine.tilemap.tilemap_error import *
from typing import *
from engine.context.context import *
import pygame

class Tilemap(GameObject):

    def __init__(self, game:GameContext, tile_size:Tuple[int, int], z_pos:float, offset:Tuple[int, int]=(0, 0)) -> None:
        """
engine.tilemap.Tilemap

Object used to manage tiles as small game components that are assigned to a position inside the Tilemap.
They can be displayed, removed, changed and they can interact with entities by colliding with them. Each 
tile has it's own ID and this ID is linked to a tileset that contains all the images for the tiles.

Args:
    tile_size : width and height of each tiles
    z_pos     : z position of each tiles
    offset    : offset to apply when placing tiles, usefull for chunks systems and terrain generation
        """
    ...

    def place_tile(self, id:int, location:Tuple[int, int], rotation:int=0, flip_x:bool=False, flip_y:bool=False) -> None:
        """
engine.tilemap.Tilemap.place_tile

Method used to place a tile on a defined location of the tilemap.

Args:
    id : id of the tile
    location : position of the tile inside the tilemap
    rotation : rotation of the tile
    flip_x : if enabled, the tile is flipped on the horizontal axis
    flip_y : if enabled, the tile is flipped on the vertical axis
        """
    ...

    def place_pattern(self, pattern, location, rotation=0, flip_x=False, flip_y=False):
        """
engine.tilemap.Tilemap.place_pattern

Method used to place a pattern on a defined location of the tilemap.
A pattern is a rectangular shape that contains tiles, it is represented
as a 2D matrix and each matrix is a tile ID.

Args :
    pattern : pattern to place
    location : top-left corner position of the pattern
    rotation : rotation of the tiles of the pattern
    flip_x : if enabled, the tiles of the pattern are flipped on the horizontal axis
    flip_y : if enabled, the tiles of the pattern are flipped on the vertical axis
        """
        ...