import pygame

class Animated:
    def __init__(self, animations, animation_speed=0.2):
        self.animation = 0
        self.animations = animations
        self.animation_speed = animation_speed
        self.animation_cursor = 0

    def animate(self, dt):
        if int(self.animation_cursor) + self.animation_speed * dt < len(self.animations[self.animation]): self.animation_cursor += self.animation_speed * dt
        else: self.animation_cursor = 0
        try: self.image = self.animations[self.animation][int(self.animation_cursor)]
        except: self.image = self.animations[self.animation][0]
    
    def get_image(self):
        return self.image
    
    def set_animation(self, animation):
        self.animation = animation
    
    def set_animation_speed(self, animation_speed):
        self.animation_speed = animation_speed
    
    def set_animation_cursor(self, animation_cursor):
        self.animation_cursor = animation_cursor

    def flip_image(self, x_flip, y_flip):
        self.image = pygame.transform.flip(self.animations[self.animation][int(self.animation_cursor)-1], x_flip, y_flip)