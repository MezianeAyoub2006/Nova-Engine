from typing import *
import pygame

class GameContext:
    camera : List[int, int]
    zoom : float 
    zoom_enabled : float
    assets : dict
    def __init__(self, resolution:Tuple[int, int], flags:int=0, vsync:bool=False):
        ...
    
    def run(self, game_loop, fill_color:Tuple[int, int, int]=(0, 0, 0)):
        ...
    
    def quit(self):
        ...

    def draw_rect(self, rect:pygame.Rect, color:Tuple[int, int, int], z_pos:Union[float, None]=None):
        ...

    def render_rect(self, rect:pygame.Rect, color:Tuple[int, int, int], z_pos:Union[float, None]=None):
        ...

    def draw(self, surface:pygame.Surface, position:Union[Tuple, List][int, int], z_pos:Union[float, None]=None):
        ...
    
    def render(self, surface:pygame.Surface, position:Union[Tuple, List][int, int], z_pos:Union[float, None]=None):
        ...
    
    def set_caption(self, text:str):
        ...

    def get_fps(self) -> float:
        ...
    
    def get_dt(self) -> float:
        ...
    
    def get_display_size(self) -> Tuple[int, int]:
        ...
    
    def get_pressed(self) -> dict:
        ...
    
    def toggle_fullscreen(self):
        ...

    def get_screen_center(self) -> Tuple[int, int]:
        ...

    def load_font(self, file:str, name:str, size:int):
        ...

    def load_sysfont(self, sysfont:str, size:int):
        ...
    
    def draw_text(self, text:str, font:str, position:Union[Tuple, List][int, int], color:Tuple[int, int, int]=(0,0,0), antialias:bool=True, draw:bool=True) -> pygame.Surface:
        ...
    
    def render_text(self, text:str, font:str, position:Union[Tuple, List][int, int], color:Tuple[int, int, int]=(0,0,0), antialias:bool=True, draw:bool=True) -> pygame.Surface:
        ...



    
    

