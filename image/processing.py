import os, pygame
from typing import *
from PIL import Image
from engine.image.slicer import Slicer, convert_PIL_pygame

PATH = ''

def set_path(path:str):
    global PATH
    PATH = path

def load_image(path:str):
    img = pygame.image.load(f'{PATH}{path}').convert_alpha()
    return img

def load_images(path:str):
    images = []
    for image_name in os.listdir(f'{PATH}/{path}'):
        images.append(load_image(f'{path}/{image_name}'))
    return images

def set_alpha(image:pygame.Surface, alpha:int):
    img = image
    img.set_alpha(alpha)
    return img

def scale_image_list(images:List[pygame.Surface], scaling:Tuple[int, int]):
    return [pygame.transform.scale(image, scaling) for image in images]

def scale_animations(animations:List[List], scaling:Tuple[int, int]):
    return [scale_image_list(images, scaling) for images in animations]

def get_outline(image:pygame.Surface, color:Tuple[int, int, int]=(0,0,0)):
    mask = pygame.mask.from_surface(image, 127)
    outline_image = pygame.Surface(image.get_size()).convert_alpha()
    outline_image.fill((0,0,0,0))
    for point in mask.outline():
        outline_image.set_at(point,color)
    return outline_image

def load_sprite(path:str, slicing:Tuple[int, int]):
    sprite = Slicer(PATH + path)
    sprite.slice_(slicing[0], slicing[1])
    return [convert_PIL_pygame(image).convert_alpha() for image in sprite.slices]

def load_animation(path:str, slicing:Tuple[int, int], frames:int):
    sprite = Slicer(PATH + path)
    sprite.slice_(slicing[0], slicing[1])
    sprite.organise(frames)
    return sprite.slices

def organise_into_animation(sprite, slicing, frames):
    slicer = Slicer()
    slicer.img = sprite
    slicer.slice_(slicing[0], slicing[1])
    slicer.organise(frames)
    return slicer.slices