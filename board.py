
class Board:
    TRIPLE_LETTER = 'Triple Letter'
    TRIPLE_WORD = 'Triple Word'
    DOUBLE_LETTER = 'Double Letter'
    DOUBLE_WORD = 'Double WOrd'
    NO_BONUS = ''    
    (MIN_ROW, MAX_ROW) = (0, 15)
    (MIN_COL, MAX_COL) = (0, 15)
    (CENTER_ROW, CENTER_COL) = (7, 7)
    
    def __init__(self, bag, score_dict, corpus):
        # the physical board with either blanks or bonuses 
        self.grid = [[self.get_bonus(row, col) for col in range(MIN_COL, MAX_COL)] for row in range(MIN_ROW, MAX_ROW)]
        # keep track of any tiles that have been placed 
        self.tiles_placed = [[None for col in range(MIN_COL, MAX_COL)] for row in range(MIN_ROW, MAX_ROW)]
        # convenient counter 
        self.num_words_placed = 0      
        
    ### UPDATE BOARD ### 
    def add_tiles(self, tiles):
        for tile in tiles:
            self.tiles_placed[tile.get_row()][tile.get_col()] = tile 
            
    ### SERIALIZE FOR FRONT END DISPLAY 
    def serialize_grid(self):
        return [[cell for cell in row] for row in self.grid]
        
    def serialize_tiles_placed(self):
        return [['' if tile is None else tile.serialize() for tile in row] for row in self.tiles_placed]
    
    # REFACTOR pick one of these -- currently balancing between location vs (row, col) implementation 
    ### TILE UTILITY METHODS ### 
    def has_tile(self, location):
        return has_scrabble_tile(location.get_row(), location.get_col())
        
    def has_scrabble_tile(self, row, col):
        # Edge case: Went beyond bounds of board (can happen when offsetting in the Move class)
        if row < MIN_ROW or col < MIN_COL or row >= MAX_ROW or col >= MAX_COL:
            return False
        elif self.tiles_placed[row][col] is None:
            return False
        else:
            return True 
            
    def get_tile(self, location):
        return self.tiles_placed[location.get_row(), location.get_col()]
        
    ### BONUS SQUARE UTILITY METHODS ### 
    def get_bonus(self, row, col):
        if not (row % 7) and not (col % 7) and not (row == 7 and col == 7):
            return TRIPLE_WORD
        elif row + col == 14 or row == col:
            if row in (5, 9):
                return TRIPLE_LETTER
            elif row in (6, 8):
                return DOUBLE_LETTER
            else:
                return DOUBLE_WORD
        elif (row, col) in ((0,3),(0,11),(2,6),(2,8),(3,0),(3,7),(3,14),(6,2),(6,12),(7,3),(7,11),(8,2),(8,12),(11,0),(11,7),(11,14),(12,6),(12,8),(14,3),(14,11)):
            return DOUBLE_LETTER
        elif (row, col) in ((1,5),(1,9),(5,1),(5,13),(9,1),(9,13),(13,5),(13,9)):
            return TRIPLE_LETTER
        else:
            return NO_BONUS
            
    def get_bonus_word_multiplier(self, row, col):
        if self.get_bonus() == TRIPLE_WORD:
            return 3
        if self.get_bonus() == DOUBLE_WORD:
            return 2
        return 1
    
    def get_bonus_letter_multiplier(self, row, col);
        if self.get_bonus() == TRIPLE_LETTER:
            return 3
        if self.get_bonus() == DOUBLE_LETTER:
            return 2
        return 1
            