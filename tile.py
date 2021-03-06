
import location 
 
class Tile:
    SCRABBLE_SCORE_DICT = dict()
    SCRABBLE_SCORE_DICT['A'] = 1
    SCRABBLE_SCORE_DICT['B'] = 3
    SCRABBLE_SCORE_DICT['C'] = 3
    SCRABBLE_SCORE_DICT['D'] = 2
    SCRABBLE_SCORE_DICT['E'] = 1
    SCRABBLE_SCORE_DICT['F'] = 4
    SCRABBLE_SCORE_DICT['G'] = 2
    SCRABBLE_SCORE_DICT['H'] = 4
    SCRABBLE_SCORE_DICT['I'] = 1
    SCRABBLE_SCORE_DICT['J'] = 8
    SCRABBLE_SCORE_DICT['K'] = 5
    SCRABBLE_SCORE_DICT['L'] = 1
    SCRABBLE_SCORE_DICT['M'] = 3
    SCRABBLE_SCORE_DICT['N'] = 1
    SCRABBLE_SCORE_DICT['O'] = 1
    SCRABBLE_SCORE_DICT['P'] = 3
    SCRABBLE_SCORE_DICT['Q'] = 10
    SCRABBLE_SCORE_DICT['R'] = 1
    SCRABBLE_SCORE_DICT['S'] = 1
    SCRABBLE_SCORE_DICT['T'] = 1
    SCRABBLE_SCORE_DICT['U'] = 1
    SCRABBLE_SCORE_DICT['V'] = 4
    SCRABBLE_SCORE_DICT['W'] = 4
    SCRABBLE_SCORE_DICT['X'] = 8
    SCRABBLE_SCORE_DICT['Y'] = 4
    SCRABBLE_SCORE_DICT['Z'] = 10    
    
    def __init__(self, letter, player = None, location = None):
        self.letter = letter
        self.player = player
        self.points = Tile.SCRABBLE_SCORE_DICT[letter]
        self.location = location 
        
    def copy_tile(self):
        return Tile(self.letter, self.player, self.location)
        
    def remove_player(self):
        self.player = None 
        return self
    
    def change_player(self, player):
        self.player = player
        return self 
    
    def change_location(self, location):
        self.location = location 
        
    def serialize(self):
        # player can be None if this is a tile in the bag 
        # location can be None if tile has not been placed on the board 
        return {'letter': self.letter, \
                'points': self.points, \
                'player': "" if self.player is None else self.player.serialize_type(), \
                'location': "" if self.location is None else self.location.serialize()}
    