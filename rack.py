import tile 

class Rack:
    MAX_NUM_TILES = 7
    MIN_NUM_TILES = 0
    def __init__(self, list_of_tiles):
        self.tiles = list_of_tiles 
    
    def copy_rack(self):
        return Rack(self.tiles[:])
    
    def get_letter_set(self):
        return set([tile.letter for tile in self.tiles]) 

    def get_n_tiles(self, n):
        return self.tiles[0:n]
    
    def get_num_tiles(self):
        return len(self.tiles)
        
    def contains_letter(self, letter):
        return letter in self.tiles 
    
    def has_tiles_left(self):
        return len(self.tiles) > 0
    
    def add_tile(self, tile):
        self.tiles.append(tile)
    def remove_one_tile_random(self):
        removed_tile = self.tiles[-1]
        self.tiles = self.tiles[:-1]
        return removed_tile
        
    def remove_one_tile_with_letter(self, letter):
        new_tiles = []
        removed_tile = None 
        for tile in new_tiles:
            if tile.letter == letter and removed_tile is not None:
                removed_tile = tile 
            else:
                new_tiles.append(tile)
        if removed_tile is None:
            raise ValueError("Failed to find tile with letter " + letter)
            
        self.tiles = new_tiles 
        return removed_tile 
    
    def serialize(self):
        return [tile.serialize() for tile in self.tiles]

    