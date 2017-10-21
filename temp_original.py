#Author: Daniel M. Cheng
#Creation: February 2016
#Description: Scrabble AI based on Steven A. Gordon's GADDAG data structure (http://ericsink.com/downloads/faster-scrabble-gordon.pdf)
#Modified: July 2017 -- set up front-end server for playing against Scrabble AI 

import os, csv, sys, random

#global gaddag so that this only loads once to server all requests 
SCRABBLE_APPRENTICE_GADDAG = scrabble_apprentice_gaddag.read_gaddag_full()



def load_all():
    scrabble_corpus = load_scrabble_corpus()
    scrabble_score_dict = load_scrabble_score_dict()
    scrabble_freq_dict = load_scrabble_freq_dict()
    scrabble_bag = load_scrabble_bag(scrabble_freq_dict)
    return (scrabble_score_dict, scrabble_freq_dict, scrabble_bag, scrabble_corpus)


        
#3: Scrabble board play class
#global vars
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

GEN_MOVES_PRINT_INDENT = "  "

#debugging/printing variables
DEBUG_PULL_VALID_CROSSWORD = False
DEBUG_GENERATE_MOVES = False
DEBUG_FINAL_CALC_SCORE = False
DEBUG_ALL_MOVES = False
        
    def clear_comp(self):
        self.comp_max_score = 0
        self.comp_max_word = []
        self.comp_max_row = None
        self.comp_max_col = None
        self.comp_max_direction = None
        self.comp_all_possible_moves = {HORIZONTAL:{}, VERTICAL:{}}
        
    
 
    def find_coordinate_bounds_of_word(self, curr_offset, hook_row, hook_col, direction, word):
        if direction == HORIZONTAL:
            #either we were offset to the beginning of the word (i.e. we hit eow on a reversed prefix)
            if curr_offset <= 0:
                (start_row, start_col) = (hook_row, hook_col + curr_offset)
            #or we were offset to the end of the word
            else:
                (start_row, start_col) = (hook_row, hook_col + curr_offset - len(word) + 1)
            (end_row, end_col) = (start_row, start_col + len(word) - 1)
        else:
            if curr_offset <= 0:
                (start_row, start_col) = (hook_row + curr_offset, hook_col)
            else:
                (start_row, start_col) = (hook_row + curr_offset - len(word) + 1, hook_col)
            (end_row, end_col) = (start_row + len(word) - 1, start_col)
        return (start_row, start_col, end_row, end_col)
       
    #checks that if we continue to concatenate, 
        #that there is NOT a tile to the left (above) or to the right (below) of this eow
    def ends_are_filled(self, curr_offset, hook_row, hook_col, direction, word, front_or_back):
        (start_row, start_col, end_row, end_col) = \
            self.find_coordinate_bounds_of_word(curr_offset, hook_row, hook_col, direction, word)
        #print(word)
        #print(str((start_row, start_col, end_row, end_col)))
        if direction == HORIZONTAL:
            (front_row, front_col) = (start_row, start_col - 1)
            (back_row, back_col) = (end_row, end_col + 1)
        else:
            (front_row, front_col) = (start_row - 1, start_col)
            (back_row, back_col) = (end_row + 1, end_col)
        if front_or_back == FRONT_END:
            return self.is_scrabble_tile(front_row, front_col)
        elif front_or_back == FRONT_OR_BACK_END:
            return self.is_scrabble_tile(front_row, front_col) or self.is_scrabble_tile(back_row, back_col)
        else:
            raise ValueError("Requested something besides FRONT_END or FRONT_OR_BACK_END")
    
    #this is called once we hit the end of a word     
    def save_word_and_score(self, curr_offset, hook_row, hook_col, direction, word, valid_crossword_score_dict, indent):
        (start_row, start_col, end_row, end_col) = self.find_coordinate_bounds_of_word(curr_offset, hook_row, hook_col, direction, word)
        
        if DEBUG_FINAL_CALC_SCORE:
            global DEBUG_PULL_VALID_CROSSWORD
            save_user_option = DEBUG_PULL_VALID_CROSSWORD
            DEBUG_PULL_VALID_CROSSWORD = True
            word_score = self.calc_word_score(start_row, start_col, direction, word, valid_crossword_score_dict)
            DEBUG_PULL_VALID_CROSSWORD = save_user_option
        word_score = self.calc_word_score(start_row, start_col, direction, word, valid_crossword_score_dict)
        #exception for the first move
        if self.num_words_placed == 0 and not self.intersect_center_tile(start_row, start_col, direction, word):
            return
        
            
        cleaned_word = ''.join(word) #make this a string for ease of reading--this dictionary isn't used for anything aside from debugging
        if (start_row, start_col) in self.comp_all_possible_moves[direction].keys():
            if cleaned_word in self.comp_all_possible_moves[direction][(start_row, start_col)].keys():
                #TBD--overlap between col and row iterations
                print(cleaned_word + " at " + str((start_row, start_col)) + " with score " + str(word_score))
                print(self.comp_all_possible_moves)
                raise ValueError("Resaving a word that was previously computer calculated with a different score")
            self.comp_all_possible_moves[direction][(start_row, start_col)][cleaned_word] = word_score
        else:
            self.comp_all_possible_moves[direction][(start_row, start_col)] = {}
            self.comp_all_possible_moves[direction][(start_row, start_col)][cleaned_word] = word_score
            
        if word_score > self.comp_max_score:
            self.comp_max_score = word_score
            self.comp_max_word = word #save this as a list since this is the standard type throughout
            self.comp_max_row = start_row
            self.comp_max_col = start_col
            self.comp_max_direction = direction
        if DEBUG_GENERATE_MOVES:
            print(indent + GEN_MOVES_PRINT_INDENT + "SAVED THIS WORD: " + cleaned_word + " at " + str((start_row, start_col)))
  
        
    def find_filled_rows_and_cols(self, placed_tiles):
        rows = set([])
        cols = set([])
        for row in range(MIN_ROW, MAX_ROW):
            for col in range(MIN_COL, MAX_COL):
                if placed_tiles[row][col] != "":
                    rows.add(row)
                    cols.add(col)
        return (rows, cols) 
        
    def convert_placed_tiles_to_full_placement(self, placed_tiles):
        (filled_rows, filled_cols) = self.find_filled_rows_and_cols(placed_tiles)
        if len(filled_rows) == 0:
            raise ValueError("You must place at least one tile. If you cannot move, exchange tiles or simply pass")
        elif len(filled_rows) == 1:
            direction = HORIZONTAL 
        elif len(filled_cols) == 1: 
            direction = VERTICAL 
        else:
            raise ValueError("You can only place in one row or column")        
        #the leftmost / uppermost point of adjacency 
        anchor_row = min(filled_rows)
        anchor_col = min(filled_cols)        
        
        #similar to the pull_valid_crossword_score function...
        prefix = self.find_word_from_anchor(placed_tiles, anchor_row, anchor_col, direction, 'PREFIX')
        suffix = self.find_word_from_anchor(placed_tiles, anchor_row, anchor_col, direction, 'SUFFIX')
        print("prefix: {0}, suffix: {1}, placed_tiles {2}, anchor_row {3}, anchor_col {4}".format(prefix, suffix, placed_tiles, anchor_row, anchor_col))
        word = prefix + [placed_tiles[anchor_row][anchor_col]] + suffix
        
        #exception for one tile placements--the official direction is the direction that creates the longer word 
        if len(word) == 1:
            flipped_direction = direction * - 1
            flipped_prefix = self.find_word_from_anchor(placed_tiles, anchor_row, anchor_col, flipped_direction, 'PREFIX')
            flipped_suffix = self.find_word_from_anchor(placed_tiles, anchor_row, anchor_col, flipped_direction, 'SUFFIX')
            flipped_word = flipped_prefix + [placed_tiles[anchor_row][anchor_col]] + flipped_suffix
            if len(flipped_word) > 1:
                word = flipped_word 
                direction = flipped_direction 
                prefix = flipped_prefix
                suffix = flipped_suffix
        #the actual start of the word -- since there would be existing tiles to the left / top of the anchor tile 
        if direction == HORIZONTAL:
            start_row = anchor_row 
            start_col = anchor_col - len(prefix)
        else:
            start_row = anchor_row - len(prefix)
            start_col = anchor_col 
            
        #check that there aren't extra tiles placed beyond the end of the word (since we walked down until finding an empty spot 
        if (max(filled_rows) > start_row + len(word) - 1) or (max(filled_cols) > start_col + len(word) - 1):
            raise ValueError("All tiles must be connected to each other") 
            
        return {"start_row": start_row, "start_col": start_col, "direction": direction, "word": word}
        
    #given the starting placement--i.e. the anchor tile--determine the prefix and suffix (since the full word may include tiles on the board) 
    def find_word_from_anchor(self, placed_tiles, anchor_row, anchor_col, direction, prefix_or_suffix):
        if direction == HORIZONTAL:
            (row_delta, col_delta) = (0, 1)
        else:
            (row_delta, col_delta) = (1, 0)
        if prefix_or_suffix == 'PREFIX':
            (row_delta, col_delta) = (row_delta * -1, col_delta * -1)
            
        word_fix = []
        (curr_row, curr_col) = (anchor_row, anchor_col)
        print("Find start for {0} at {1} {2}".format(word_fix, curr_row, curr_col))
        while True:
            (curr_row, curr_col) = (curr_row + row_delta, curr_col + col_delta)
            if curr_row >= MIN_ROW and curr_row < MAX_ROW and curr_col >= MIN_COL and curr_col < MAX_COL:
                if self.is_scrabble_tile(curr_row, curr_col):
                    letter = self.board[curr_row][curr_col]
                else:
                    letter = placed_tiles[curr_row][curr_col]
                print(curr_row, curr_col, letter) 
                if letter != "":
                    word_fix.append(letter) #insert in front
                else:
                    break
            else:
                break
        print(word_fix) 
        if prefix_or_suffix == 'PREFIX':
            return word_fix[::-1]
        return word_fix 

        
          
if __name__ == "__main__":
    scrabble_corpus = load_scrabble_corpus()
    scrabble_apprentice_gaddag.write_gaddag_full(scrabble_corpus)

    
    
