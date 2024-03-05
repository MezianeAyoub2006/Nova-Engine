from numpy import array, int64, flip, rot90

class Pattern:
    def __init__(self, data):
        self.data = data

    def get_size(self):
        return (len(self.data[0][0]), len(self.data[0]), len(self.data))
    
    def get_overlap_offsets(self):
        overlap_offsets = []
        steps = self.get_size()
        for x in range(-steps[0]+1, steps[0]):
            for y in range(-steps[1]+1, steps[1]):
                overlap_offsets.append((x, y))
        return overlap_offsets
    
    def flip(self, axis):
        self.data = flip(self.data, {"h" : 1, "v" : 0}[axis])
    
    def rotate(self, rotations):
        self.data  = rot90(self.data, rotations, (0, 1))