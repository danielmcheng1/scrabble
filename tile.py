
#TBD player name, type, or ID?    
class tile:
    SCRABBLE_SCORE_DICT = load_scrabble_score_dict()
    def __init__(self, letter, player, location):
        self.letter = letter
        self.player = player
        self.points = SCRABBLE_SCORE_DICT[letter]
        self.location = location 
        
    def serialize(self):
        return {'letter': self.letter, 'points': self.points, 'player': self.player.serialize, 'location': self.location.serialize}

        
    def load_scrabble_score_dict():
        scrabble_score_dict = dict()
        
        scrabble_score_dict[WILDCARD] = 0
        scrabble_score_dict['A'] = 1
        scrabble_score_dict['B'] = 3
        scrabble_score_dict['C'] = 3
        scrabble_score_dict['D'] = 2
        scrabble_score_dict['E'] = 1
        scrabble_score_dict['F'] = 4
        scrabble_score_dict['G'] = 2
        scrabble_score_dict['H'] = 4
        scrabble_score_dict['I'] = 1
        scrabble_score_dict['J'] = 8
        scrabble_score_dict['K'] = 5
        scrabble_score_dict['L'] = 1
        scrabble_score_dict['M'] = 3
        scrabble_score_dict['N'] = 1
        scrabble_score_dict['O'] = 1
        scrabble_score_dict['P'] = 3
        scrabble_score_dict['Q'] = 10
        scrabble_score_dict['R'] = 1
        scrabble_score_dict['S'] = 1
        scrabble_score_dict['T'] = 1
        scrabble_score_dict['U'] = 1
        scrabble_score_dict['V'] = 4
        scrabble_score_dict['W'] = 4
        scrabble_score_dict['X'] = 8
        scrabble_score_dict['Y'] = 4
        scrabble_score_dict['Z'] = 10
      
        return scrabble_score_dict
        