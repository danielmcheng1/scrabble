import random 
import tile 

class Bag:
    def __init__(self):
        self.bag = []
        tile_freq_dict = self.load_tile_freq_dict()
        for letter in tile_freq_dict.keys():
            self.bag = self.bag + [tile.Tile(letter)] * tile_freq_dict[letter]
        self.shuffle_bag()
        
    def shuffle_bag(self):
        random.shuffle(self.bag)
    
    # for randomness, assumes bag was shuffled beforehand 
    def draw_tile(self):
        return self.bag.pop() 
        
    def num_tiles_left(self):
        return len(self.bag) 
        
    def has_tiles_left(self):
        return len(self.bag) > 0 
        
    def load_tile_freq_dict(self):
        tile_freq_dict = dict()
        
        tile_freq_dict['A'] = 9
        tile_freq_dict['B'] = 2
        tile_freq_dict['C'] = 2
        tile_freq_dict['D'] = 4
        tile_freq_dict['E'] = 12
        tile_freq_dict['F'] = 2
        tile_freq_dict['G'] = 3
        tile_freq_dict['H'] = 2
        tile_freq_dict['I'] = 9
        tile_freq_dict['J'] = 1
        tile_freq_dict['K'] = 1
        tile_freq_dict['L'] = 4
        tile_freq_dict['M'] = 2
        tile_freq_dict['N'] = 6
        tile_freq_dict['O'] = 8
        tile_freq_dict['P'] = 2
        tile_freq_dict['Q'] = 1
        tile_freq_dict['R'] = 6
        tile_freq_dict['S'] = 4
        tile_freq_dict['T'] = 6
        tile_freq_dict['U'] = 4
        tile_freq_dict['V'] = 2
        tile_freq_dict['W'] = 2
        tile_freq_dict['X'] = 1
        tile_freq_dict['Y'] = 2
        tile_freq_dict['Z'] = 1

        return tile_freq_dict
