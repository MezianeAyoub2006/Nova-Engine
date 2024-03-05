import pygame, sys, os, time, math
from typing import *
from engine.other.draw_object import *

class GameContext:
    def __init__(self, resolution:Tuple[int, int], flags:int=0, vsync:bool=False):
        pygame.init()
        pygame.display.set_caption("nova engine project")
        self.screen = pygame.display.set_mode(resolution, flags, vsync=vsync)
        self.rendering_surface = pygame.Surface(resolution, pygame.SRCALPHA)
        self.drawing_surface = pygame.Surface(resolution, pygame.SRCALPHA)
        self.background_surface = pygame.Surface(resolution, pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.camera = [0, 0]
        self.freeze = False
        self.zoom_enabled = True
        self.zoom = 1
        self.fonts = {}
        self.dt = 1
        self.lt = time.perf_counter()
        self.scroll_ = [0, 0]
        self.rendering_offset = (0, 0)

    def run(self, game_loop):
        while 1:
            self.delta_time()
            if self.zoom_enabled and self.zoom != 1:
                self.rendering_size = (self.screen.get_size()[0]/self.zoom + (self.get_display_size()[0]/6.4)/self.zoom, self.screen.get_size()[1]/self.zoom + (self.get_display_size()[1]/3.6)/self.zoom)
                self.rendering_surface = pygame.Surface(self.rendering_size, pygame.SRCALPHA)
                self.rendering_rect = self.rendering_surface.get_rect(center=self.get_screen_center())
                self.rendering_vector = pygame.math.Vector2(self.rendering_size)
                self.rendering_offset = (self.rendering_size[0] // 2 - self.get_screen_center()[0], self.rendering_size[1] // 2 - self.get_screen_center()[1])
                game_loop()
                scaled_surf = pygame.transform.scale(self.rendering_surface, self.rendering_vector*self.zoom)
                scaled_rect = scaled_surf.get_rect(center = (self.get_screen_center()[0], self.get_screen_center()[1]))
                self.screen.blit(self.background_surface, (0, 0))
                self.screen.blit(scaled_surf, scaled_rect)
            else:
                self.rendering_surface.fill((0,0,0,0))
                game_loop()
                self.screen.blit(self.background_surface, (0, 0))
                self.screen.blit(self.rendering_surface, (0, 0))
            self.screen.blit(self.drawing_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(10000)

    def quit(self):
        pygame.quit()
        sys.exit()

    def delta_time(self):
        self.dt = time.perf_counter() - self.lt
        self.dt *= 60
        self.lt = time.perf_counter()
    
    def draw_rect(self, rect:pygame.Rect, color:Tuple[int, int, int], z_pos:Union[float, None]=None):
        if z_pos == None:
            pygame.draw.rect(self.drawing_surface, color, rect)

    def render_rect(self, rect:pygame.Rect, color:Tuple[int, int, int], z_pos:Union[float, None]=None):
        srf = pygame.Surface((rect.w, rect.h))
        srf.fill(color)
        if z_pos == None:
            self.render(srf, (rect.x, rect.y))

    def draw(self, surface:pygame.Surface, position, z_pos=None, scene=None):
        self.drawing_surface.blit(surface, position)
    
    def background_draw(self, surface:pygame.Surface, position, z_pos=None, scene=None):
        if z_pos == None:
            self.background_surface.blit(surface, position)
        else:
            scene.link(BackgroundDrawObject(self, surface, position, z_pos))

    def render(self, surface:pygame.Surface, position, z_pos:Union[float, None]=None, scene=None, absolute=False):
        if z_pos == None:
            if absolute:
                self.rendering_surface.blit(surface, position)
            else:
                self.rendering_surface.blit(surface, self.relative(position))
        else:
            scene.link(RenderObject(self, surface, position, z_pos))

    def set_caption(self, text:str):
        pygame.display.set_caption(text)

    def get_fps(self) -> float:
        return self.clock.get_fps()
    
    def get_dt(self) -> float:
        return self.dt
    
    def get_display_size(self) -> Tuple[int, int]:
        return self.screen.get_size()
    
    def relative(self, position):
        screen_size = self.screen.get_size()
        rendering_x = position[0] + screen_size[0]/2 - self.camera[0] + self.rendering_offset[0]
        rendering_y = position[1] + screen_size[1]/2 - self.camera[1] + self.rendering_offset[1]
        return [rendering_x, rendering_y]

    def get_pressed(self) -> dict:
        return pygame.key.get_pressed()

    def toggle_fullscreen(self):
        pygame.display.toggle_fullscreen()

    def scroll(self, position, scroll_speed):
        self.scroll_[0] += ((position[0] - self.scroll_[0]) / scroll_speed) * self.get_dt()
        self.camera = [int(self.scroll_[0]), self.camera[1]]
        self.scroll_[1] += (position[1] - self.scroll_[1]) / scroll_speed * self.get_dt()
        self.camera = [self.camera[0], int(self.scroll_[1])]
    
    def get_screen_center(self) -> Tuple[int, int]:
        return (self.screen.get_size()[0]/2, self.screen.get_size()[1]/2)
    
    def load_font(self, file:str, name:str, size:int):
        txt = name
        txt += str(size)
        self.fonts[txt] = pygame.font.Font(file, size)

    def load_sysfont(self, sysfont:str, size:int):
        txt = sysfont
        txt += str(size)
        self.fonts[txt] = pygame.font.SysFont(sysfont, size)

    def draw_text(self, text:str, font:str, position, color:Tuple[int, int, int]=(0,0,0), antialias:bool=True, draw:bool=True) -> pygame.Surface:
        font = self.fonts[font]
        if draw:
            self.drawing_surface.blit(font.render(text, antialias, color), position)
        return font.render(text, antialias, color)

    def render_text(self, text:str, font:str, position, color:Tuple[int, int, int]=(0,0,0), antialias:bool=True, draw:bool=True) -> pygame.Surface:
        font = self.fonts[font]
        if draw:
            self.rendering_surface.blit(font.render(text, antialias, color), self.relative(position))
        return font.render(text, antialias, color)