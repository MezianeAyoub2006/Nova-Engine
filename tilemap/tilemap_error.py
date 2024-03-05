class TilemapError(Exception):
    def __init__(self, message, loc, layer):
        super().__init__(message+f"(x={loc[0]}, y={loc[1]})")