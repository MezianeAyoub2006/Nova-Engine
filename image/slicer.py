import pygame
from PIL import Image

def convert_PIL_pygame(img:pygame.Surface):
    mode = img.mode
    size = img.size
    data = img.tobytes()
    return pygame.image.fromstring(data, size, mode)

class Slicer:
    def __init__(self, img:str):
        self.img = Image.open(img)

    def slice_(self, x:int, y:int):    
            width, height = self.img.size
            slices = []
            for i in range(0, height, y):
                for j in range(0, width, x):
                    box = (j, i, j+x, i+y)
                    slices.append(self.img.crop(box))
            self.slices = slices

    def organise(self, y:int):
        m=[]
        for i in range(len(self.slices)//y):
            m.append(self.slices[i*y: (i+1)*y])
        for i in m:
            ni = [image for image in i if not all(p[3] == 0 for p in image.getdata())]
            i[:] = ni
        for i in range(len(m)):
            for j in range(len(m[i])):
                m[i][j] = convert_PIL_pygame(m[i][j]).convert_alpha()
        self.slices = m