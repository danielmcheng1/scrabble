#Author: Daniel M. Cheng
#Creation: February 2016
#Description: Scrabble AI based on Steven A. Gordon's GADDAG data structure (http://ericsink.com/downloads/faster-scrabble-gordon.pdf)
#Modified: July 2017 -- set up front-end server for playing against Scrabble AI 

import os, csv, sys, random

#global gaddag so that this only loads once to server all requests 
SCRABBLE_APPRENTICE_GADDAG = scrabble_apprentice_gaddag.read_gaddag_full()


        
    
    
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

    
    
