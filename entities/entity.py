from engine.core.game_object import *
from engine.context.context import *
import pygame, math

class Entity(GameObject):
    def __init__(self, game, pos, size, offset, z_pos):
        GameObject.__init__(self, game, z_pos)
        self.pos = pos
        self.size = size
        self.offset = offset
        self.tags.append("@entity")
        self.collide = False
        self.vel = [0, 0]
        self.slope_offsets = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        self.contact_area = {"up" : 1, "down" : 1, "right" : 1, "left" : 1}
        self.contact_tolerence = {"up" : 1, "down" : 1, "right" : 10, "left" : 10}
        self.collisions = {'up': [], 'down': [], 'right': [], 'left': []}
        self.ramp_collisions = []
        self.image = pygame.Surface((0, 0))

    def get_tiles(self, scene, tags):
        for tilemap in scene.get_objects_by_tags("@tilemap", *tags):
            for tile_rect, tile_id, tile_properties in tilemap.get_tiles_around(self.rect().center):
                yield tile_rect, tile_id, tile_properties

    def create_contact_rects(self):
        contacts = {}
        self_rect = self.rect()
        contacts["up"] = pygame.Rect(self_rect.left+self_rect.w*(1-self.contact_area["up"])/2, self_rect.top - self.contact_tolerence["up"], self_rect.w*self.contact_area["up"], self.contact_tolerence["up"])
        contacts["down"] = pygame.Rect(self_rect.left+self_rect.w*(1-self.contact_area["down"])/2, self_rect.bottom, self_rect.w*self.contact_area["down"], self.contact_tolerence["down"])
        contacts["right"] = pygame.Rect(self_rect.right, self_rect.top+self_rect.h*(1-self.contact_area["right"])/2, self.contact_tolerence["right"], self_rect.h*self.contact_area["right"])
        contacts["left"] = pygame.Rect(self_rect.left-self.contact_tolerence["left"], self_rect.top+self_rect.h*(1-self.contact_area["left"])/2, self.contact_tolerence["left"], self_rect.h*self.contact_area["left"])
        return contacts

    def check_contact_tiles(self, scene):
        self.collisions = {'up': [], 'down': [], 'right': [], 'left': []}
        contacts = self.create_contact_rects()
        if self.collide:
            for tile_rect, tile_id, tile_properties in self.get_tiles(scene, "#solid"):
                if not "slope" in tile_properties: 
                    for rect in contacts:
                        if contacts[rect].colliderect(tile_rect):
                            self.collisions[rect].append({"rect" : tile_rect, "id" : tile_id, "properties" : tile_properties})
                else:
                    slope = eval(tile_properties["slope"])
                    for rect in contacts:
                        if contacts[rect].colliderect(tile_rect):
                            minimal_height = self.get_minimal_height(tile_properties, tile_rect)
                            for offset in self.slope_offsets:
                                for point in ((contacts[rect].bottom+offset[1], contacts[rect].left+offset[0]), (contacts[rect].bottom+offset[1], contacts[rect].right+offset[0])):
                                    if point[0] > minimal_height:
                                        self.collisions["down"].append({"id" : tile_id, "slope" : slope, "properties" : tile_properties})

    def update(self, scene):
        self.horizontal_physics(scene)
        self.vertical_physics(scene)
        self.check_contact_tiles(scene)
        self.ramps_physics(scene)

    def get_minimal_height(self, tile_properties, tile_rect):
        slope = eval(tile_properties["slope"])
        if "origin" in tile_properties:
            origin = eval(tile_properties["origin"])
        else:
            origin = 0
        player_rect = self.rect()
        if slope > 0:
            return -slope*(player_rect.right - tile_rect.left) + tile_rect.bottom - origin * tile_rect.h * slope
        else:
            return -slope*(player_rect.left - tile_rect.right) + tile_rect.bottom  + origin * tile_rect.h * slope

    def ramps_physics(self, scene):
        for tile_rect, _, tile_properties in self.get_tiles(scene, "#solid"):
            if "slope" in tile_properties:
                if self.rect().colliderect(tile_rect):            
                    minimal_height = self.get_minimal_height(tile_properties, tile_rect)
                    player_rect = self.rect()
                    if player_rect.bottom > minimal_height:
                        player_rect.bottom = minimal_height
                    self.pos[1] = player_rect.y - self.offset[1]

    def horizontal_physics(self, scene):
        self.pos[0] += self.vel[0] * self.game.get_dt()
        rect = self.rect()
        if self.collide:
            for tile, tile_id, tile_properties in self.get_tiles(scene, "#solid"):
                if not "slope" in tile_properties:
                    tile_rect, _ = tile, tile_id
                    if rect.colliderect(tile_rect):
                        if self.vel[0] > 0:
                            rect.right = tile_rect.left
                        if self.vel[0] < 0:
                            rect.left = tile_rect.right
                        self.pos[0] = rect.x - self.offset[0]
    
    def vertical_physics(self, scene):
        self.pos[1] += self.vel[1] * self.game.get_dt()
        rect = self.rect()
        if self.collide:
            for tile, tile_id, tile_properties in self.get_tiles(scene, "#solid"):
                if not "slope" in tile_properties:
                    tile_rect, _ = tile, tile_id
                    if rect.colliderect(tile_rect):
                        if self.vel[1] > 0:
                            rect.bottom = tile_rect.top
                        if self.vel[1] < 0:
                            rect.top = tile_rect.bottom
                        self.pos[1] = rect.y - self.offset[1]
                
    def rect(self):
        return pygame.Rect(self.pos[0] + self.offset[0], self.pos[1] + self.offset[1], self.size[0], self.size[1])
    
    def debug_rect(self, color=(255,0,0)):
        image = pygame.Surface((self.size[0], self.size[1]))
        image.fill(color)
        self.game.render(image, [math.floor(self.pos[0] + self.offset[0]), math.floor(self.pos[1] + self.offset[1])])

    def render(self):
        self.game.render(self.image, (math.floor(self.pos[0] - self.offset[0]), math.floor(self.pos[1] - self.offset[1])))

    def on_screen(self):
        cam = self.game.camera
        dsp = self.game.get_display_size()
        posx = self.rect().centerx
        posy = self.rect().centery
        return posx + 32 > cam[0] and posx - 32 < cam[0] + dsp[0] and posy + 32 > cam[1] and posy - 32 < cam[1] + dsp[1]

