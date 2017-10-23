import random 
import tile 
class Bag:
    def __init__(self):
        self.bag = []
        scrabble_freq_dict = load_scrabble_freq_dict()
        for letter in scrabble_freq_dict.keys():
            self.bag = self.bag + [tile.Tile(letter, None, None)] * scrabble_freq_dict[letter]
        self.shuffle_bag()
        
    def shuffle_bag(self):
        random.shuffle(bag)
    
    # for randomness, assumes bag was shuffled beforehand 
    def draw_tile(self):
        bag.pop() 
        
    def num_tiles_left(self):
        return len(bag) 
        
    def has_tiles_left(self):
        return len(self.bag) > 0 
        
    def load_scrabble_freq_dict():
        scrabble_freq_dict = dict()
        
        scrabble_freq_dict[WILDCARD] = 0
        scrabble_freq_dict['A'] = 9
        scrabble_freq_dict['B'] = 2
        scrabble_freq_dict['C'] = 2
        scrabble_freq_dict['D'] = 4
        scrabble_freq_dict['E'] = 12
        scrabble_freq_dict['F'] = 2
        scrabble_freq_dict['G'] = 3
        scrabble_freq_dict['H'] = 2
        scrabble_freq_dict['I'] = 9
        scrabble_freq_dict['J'] = 1
        scrabble_freq_dict['K'] = 1
        scrabble_freq_dict['L'] = 4
        scrabble_freq_dict['M'] = 2
        scrabble_freq_dict['N'] = 6
        scrabble_freq_dict['O'] = 8
        scrabble_freq_dict['P'] = 2
        scrabble_freq_dict['Q'] = 1
        scrabble_freq_dict['R'] = 6
        scrabble_freq_dict['S'] = 4
        scrabble_freq_dict['T'] = 6
        scrabble_freq_dict['U'] = 4
        scrabble_freq_dict['V'] = 2
        scrabble_freq_dict['W'] = 2
        scrabble_freq_dict['X'] = 1
        scrabble_freq_dict['Y'] = 2
        scrabble_freq_dict['Z'] = 1

        return scrabble_freq_dict
