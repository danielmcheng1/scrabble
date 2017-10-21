import random 
class Bag:
    def __init__(self):
        self.bag = load_scrabble_bag() 
        
    def load_scrabble_bag():
        scrabble_bag = []
        for letter in scrabble_freq_dict.keys():
            scrabble_bag = scrabble_bag + [letter] * scrabble_freq_dict[letter]
        random.shuffle(scrabble_bag)
        return scrabble_bag
    def count_tiles_left(self):
        return len(scrabble_bag) 
        
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
