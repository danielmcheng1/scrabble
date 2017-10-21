
class Board:
    WILDCARD = ' ' #this are the two blank Scrabble tiles
    HORIZONTAL = 1
    VERTICAL = -1 #lose the benefit of boolean logic, but then you can multiply by -1 to flip
    TRIPLE_LETTER = '3L'
    TRIPLE_WORD = '3W'
    DOUBLE_LETTER = '2L'
    DOUBLE_WORD = '2W'
    NO_BONUS = '  '
    BINGO_BONUS = 50
    RACK_MAX_NUM_TILES = 7
    (MIN_ROW, MAX_ROW) = (0, 15)
    (MIN_COL, MAX_COL) = (0, 15)
    MAX_TURNS_PASSED = 6
    (CENTER_ROW, CENTER_COL) = (7, 7)

    FRONT_END = 1 #for checking if the spot before the first tile is filled
    FRONT_OR_BACK_END = 2 #for checking if the spots before and after the word are filled

    #highest for loop appears first!! http://rhodesmill.org/brandon/2009/nested-comprehensions/
    def __init__(self, bag, score_dict, corpus):
        self.board = [[self.add_premium(row, col) for col in range(MIN_COL, MAX_COL)] for row in range(MIN_ROW, MAX_ROW)]
        self.board_to_player = [["" for col in range(MIN_COL, MAX_COL)] for row in range(MIN_ROW, MAX_ROW)]
        self.num_words_placed = 0
        self.bag = bag
        self.scrabble_score_dict = score_dict
        self.scrabble_corpus = corpus
        
    def add_premium(self, row, col):
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
            
            
    #exception for the first move
    def intersect_center_tile(self, start_row, start_col, direction, word):
        if direction == HORIZONTAL:
            if start_row != 7 or start_col > CENTER_COL or start_col + len(word) - 1 < CENTER_COL:
                return False
        else:
            if start_col != 7 or start_row > CENTER_ROW or start_row + len(word) - 1 < CENTER_ROW:
                return False
        return True
            
    
    #TBD: false for beyond boudnaries seems dangerous
    def is_scrabble_tile(self, row, col):
        #went beyond bounds of board--useful when checking valid anchor squares and whether the ends are filled
        #we have to make this explicit or else board[-1] will wrap around!!
        if row < MIN_ROW or col < MIN_COL or row >= MAX_ROW or col >= MAX_COL:
            return False
        elif self.board[row][col].isalpha():
            return True
        else:
            return False