"""
This package is a pygame based game engine that provide multiples functionalities to help you making your dream game. 
You don't have to worry about implementing complex things such as scenes, tilemaps, animations, chunks system, etc...
The engine handle all theses functionalities as game components that you can use whenever you want.
You can create your own custom objects pretty easily and make them work with existing ones so the only limit is your creativity.
"""

from .image.slicer import *
from .image.processing import *
from .context.context import *
from .tilemap.tilemap import *
from .core.scene import *
from .entities.entity import *
from .entities.animated import *
from .other.utils import *
from .tilemap.management.collection import *
from .tilemap.management.pattern import *
from .other.timer import *
from .map.tiled import *
from .other.draw_object import *
from .other.parallax import *