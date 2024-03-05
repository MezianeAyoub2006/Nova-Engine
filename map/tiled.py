import xmltodict
from engine.tilemap.management.pattern import *

def list_to_matrix(list, xcount):
    matrix=[]
    for i in range(len(list)//xcount):
        matrix.append(list[i*xcount: (i+1)*xcount])
    return matrix

def tiled_to_pattern(path):
    pattern = []
    with open(path, "r") as file:
        data = xmltodict.parse(file.read())
        if "map" in data:
            data = data["map"]
    if isinstance(data["layer"], list):
        for layer in data["layer"]:
            modified_layer = [None if int(i) == 0 else int(i)-1 for i in layer["data"]["#text"].strip().split(",")]
            pattern.append(list_to_matrix(modified_layer, int(layer["@width"])))
    else:
        modified_layer = [None if int(i) == 0 else int(i)-1 for i in data["layer"]["data"]["#text"].strip().split(",")]
        pattern.append(list_to_matrix(modified_layer, int(data["layer"]["@width"])))
    return Pattern(pattern)

def load_tiled(map_path, tileset_path):
    pattern = tiled_to_pattern(map_path)
    with open(map_path, "r") as file:
        file_data = xmltodict.parse(file.read())["map"]
        file_data["objectgroup"]
        size = (int(file_data["@width"]), int(file_data["@height"]))
    with open(tileset_path, "r") as file:
        tileset_data = xmltodict.parse(file.read())["tileset"]
    return {"size" : size, "pattern" : pattern, "tileset_data" : tiled_process_tileset_data(tileset_data["tile"])}

def tiled_process_tileset_data(tileset_data):
        data = {}
        for tile in tileset_data:
            data[int(tile["@id"])] = {}
            if isinstance(tile["properties"]["property"], list):
                for property in tile["properties"]["property"]:
                    data[int(tile["@id"])][property["@name"]] = property["@value"]
            if isinstance(tile["properties"]["property"], dict):
                data[int(tile["@id"])][tile["properties"]["property"]["@name"]] = tile["properties"]["property"]["@value"]
        return data