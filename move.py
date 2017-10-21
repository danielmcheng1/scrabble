
class Move: 
    
    def __init__(self, player, tiles):
        self.comp_max_score = 0
        self.comp_max_word = []
        self.comp_max_row = None
        self.comp_max_col = None
        self.comp_max_direction = None
        self.comp_all_possible_moves = {HORIZONTAL:{}, VERTICAL:{}}
        if player.is_human():
            self.make_human_move(tiles)
        else:
            self.make_computer_move()
    def get_result(self):
        result = {}
        result["player"] = self.player 
        result["action"] = "FINISHED MOVE"
        result["detail"] = "SCRABBLE"
        result["success"] = True 
           
#################

def make_human_move(self, start_row, start_col, direction, word, player):
    print(start_row, start_col, direction, word) 
    num_tiles = len(word)
    if direction == HORIZONTAL:
        end_row = start_row + 1
        end_col = start_col + num_tiles
        cross_direction_description = "vertically"
    else:
        end_row = start_row + num_tiles
        end_col = start_col + 1
        cross_direction_description = "horizontally"

    #validity checks
    if self.is_valid_word(word):
        #pull these regardless of whether words have been placed, b/c we need these to calculate the score
        valid_hook_spots = self.pull_hooks(start_row, start_col, direction, player.rack)
        valid_crossword_score_dict = self.pull_crosswords(start_row, start_col, direction, player.rack)
        #exception for first move
        if self.num_words_placed == 0:
            if not self.intersect_center_tile(start_row, start_col, direction, word):
                raise ValueError("The first move on the board must intersect the center tile")
        #all other moves
        else:
            hooks_onto_tile = False
            for curr_row in range(start_row, end_row):
                for curr_col in range(start_col, end_col):
                    to_place = word[curr_row - start_row + curr_col - start_col] #the extra blank padding only appears when printing
                    if self.is_scrabble_tile(curr_row, curr_col):
                        if self.board[curr_row][curr_col] != to_place:
                            raise ValueError('Your tile {0} overlaps existing tiles on the board (perhaps from a concurrent session?)'.format(to_place))
                        else:
                            hooks_onto_tile = True
                    else:
                        if (curr_row, curr_col) not in valid_crossword_score_dict.keys():
                            raise ValueError("Your placed tile {0} fails to form a valid crossword going {1}".format(to_place, cross_direction_description))
                        elif to_place not in valid_crossword_score_dict[(curr_row, curr_col)].keys():
                            raise ValueError("Your placed tile {0} fails to form a valid crossword going {1}".format(to_place, cross_direction_description))
                        if (curr_row, curr_col) in valid_hook_spots:
                            hooks_onto_tile = True
            #check if we connected to a tile at some point in the word
            if not hooks_onto_tile:
                raise ValueError("Your tiles must be placed adjacent to at least one tile on the board")
    else:
        if len(word) < MIN_WORD_LENGTH:
            raise ValueError("{0} is not a valid word. Words must be at least {1} characters long".format("".join(word), MIN_WORD_LENGTH))
        else:
            raise ValueError("{0} is not a valid word in the TWL06 Scrabble dictionary".format("".join(word)))
                    
    #score and place word
    human_score = self.calc_word_score(start_row, start_col, direction, word, valid_crossword_score_dict)
    self.place_word(start_row, start_col, direction, word, player)
    return human_score
    
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
    
def find_filled_rows_and_cols(self, placed_tiles):
    rows = set([])
    cols = set([])
    for row in range(MIN_ROW, MAX_ROW):
        for col in range(MIN_COL, MAX_COL):
            if placed_tiles[row][col] != "":
                rows.add(row)
                cols.add(col)
    return (rows, cols) 
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

    
#################
def make_computer_move(self, player):        
    self.generate_all_possible_moves(player.rack)
    if self.comp_max_word:
        self.place_word(self.comp_max_row, self.comp_max_col, self.comp_max_direction, self.comp_max_word, player)
    return (self.comp_max_score, self.comp_max_word)

def generate_all_possible_moves(self, rack):
           
    for row in range(MIN_ROW, MAX_ROW):
        valid_hook_spots = self.pull_hooks(start_row, start_col, direction, player.rack)
        valid_crossword_score_dict = self.pull_crosswords(start_row, start_col, direction, player.rack)
            
        prev_hook_spot = MIN_COL
        for (hook_row, hook_col) in valid_hook_spots:
            if DEBUG_ALL_MOVES:
                print("Generating moves for this hook spot: " + str((hook_row, hook_col)))
            self.generate_moves_for_hook_spot(None, rack, [], 0, hook_row, hook_col, \
                                              HORIZONTAL, prev_hook_spot, valid_crossword_score_dict, "")
            prev_hook_spot = hook_col + 1
        if DEBUG_ALL_MOVES:
            print("\nAll possible moves to play for row: " + str(row))
            print(str(board.comp_all_possible_moves[HORIZONTAL]))
    


    for col in range(MIN_COL, MAX_COL):
        valid_hook_spots = self.pull_hooks(start_row, start_col, direction, player.rack)
        valid_crossword_score_dict = self.pull_crosswords(start_row, start_col, direction, player.rack)    
        prev_hook_spot = MIN_ROW
        for (hook_row, hook_col) in valid_hook_spots:
            if DEBUG_ALL_MOVES:
                print("Generating moves for this hook spot: " + str((hook_row, hook_col)))
            self.generate_moves_for_hook_spot(None, rack, [], 0, hook_row, hook_col, \
                                              VERTICAL, prev_hook_spot, valid_crossword_score_dict, "")
            prev_hook_spot = hook_row + 1
        if DEBUG_ALL_MOVES:
            print("\nAll possible moves to play for col: " + str(col))
            print(str(board.comp_all_possible_moves[VERTICAL]))

            
def generate_moves_for_hook_spot(self, curr_node, curr_rack, curr_word, 
                   curr_offset, hook_row, hook_col, direction, boundary,
                   valid_crossword_score_dict, indent):        
    if direction == HORIZONTAL:
        (curr_row, curr_col) = (hook_row, hook_col + curr_offset)
    else:
        (curr_row, curr_col) = (hook_row + curr_offset, hook_col)

    if DEBUG_GENERATE_MOVES:
        print(indent + "Entering generate moves at: " + str((curr_row, curr_col)) + \
              " with word " + str(curr_word) + " in current rack: " + str(curr_rack))
    #stop placing if we've reached the previous hook spot (or if we pass the max boundary of the board)
    if (direction == HORIZONTAL and curr_col < boundary) or \
       (direction == VERTICAL and curr_row < boundary) or \
       (curr_col >= MAX_COL) or (curr_row >= MAX_ROW):
        if DEBUG_GENERATE_MOVES:
            print (indent + GEN_MOVES_PRINT_INDENT + "reached a boundary")
        return
    
    #if there is already a tile here, try to place this as the next move
    if self.is_scrabble_tile(curr_row, curr_col):
        letter = self.board[curr_row][curr_col]
        if DEBUG_GENERATE_MOVES:
            print(indent + GEN_MOVES_PRINT_INDENT + "found an existing tile " + letter + " at " + str((curr_row, curr_col)))
        #read in the gaddag file for this letter 
        if curr_node is None:
            #curr_node = scrabble_apprentice_gaddag.read_gaddag_by_letter(letter).start_node
            curr_node = SCRABBLE_APPRENTICE_GADDAG.start_node
        self.concatenate_next(letter, curr_node, curr_rack, curr_word,
                   curr_offset, hook_row, hook_col, direction, boundary,
                   valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT + GEN_MOVES_PRINT_INDENT)

    #otheriwse, if we still have tiles left, try to place
    elif curr_rack:
        #iterate over the set of valid crossletters
        if (curr_row, curr_col) in valid_crossword_score_dict.keys():
            for letter in valid_crossword_score_dict[(curr_row, curr_col)].keys():
                if DEBUG_GENERATE_MOVES:
                    print(indent + GEN_MOVES_PRINT_INDENT + "trying to find letter " + letter + \
                          " with word " + str(curr_word) + " in current rack: " + str(curr_rack))
                if letter in curr_rack:
                    new_rack = curr_rack[:]
                    new_rack.remove(letter)
                    if DEBUG_GENERATE_MOVES:
                        print(indent + GEN_MOVES_PRINT_INDENT + "found letter " + letter + "--new rack is " + str(new_rack))
                    #read in the gaddag file for this letter 
                    if curr_node is None:
                        #curr_node = scrabble_apprentice_gaddag.read_gaddag_by_letter(letter).start_node
                        curr_node = SCRABBLE_APPRENTICE_GADDAG.start_node
                    self.concatenate_next(letter, curr_node, new_rack, curr_word,
                               curr_offset, hook_row, hook_col, direction, boundary,
                               valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT + GEN_MOVES_PRINT_INDENT)
    
    
#################    
#REFACTOR this places the word on the board  -- EASILY SIMPLIFY --- just place, no errors at this point 
#REFACTOR should just take input of tiles--then  the position is taken care of, no need to have direction, computer methods don't need this, etc. 
#e.g. two of the checks below can be moved out at least to the beginning of the move
    #...and maybe checking if is a word
def place_word(self, start_row, start_col, direction, word, player):
    num_tiles = len(word) 
    if direction == HORIZONTAL:
        end_row = start_row + 1
        end_col = start_col + num_tiles
    else:
        end_row = start_row + num_tiles
        end_col = start_col + 1
        
    #check that these tiles fit the board
    if (start_row < MIN_ROW or start_col < MIN_COL) or (end_row > MAX_ROW or end_col > MAX_COL) :
        raise ValueError('Word does not fit on the board')
    if num_tiles < MIN_WORD_LENGTH:
        raise ValueError('Word is too short. The minimum word length is ' + str(MIN_WORD_LENGTH) + " letters")
        
    #place in this given row or col, 
    #but break if you overlap an existing tile (and your input letters do not match up with those tiles)
    (saved_row, saved_col) = (self.board[start_row][:], self.board[:][start_col])
    for curr_row in range(start_row, end_row):
        for curr_col in range(start_col, end_col):
            to_place = word[curr_row - start_row + curr_col - start_col] #the extra blank padding only appears when printing
            if not to_place.isalpha():
                (self.board[start_row][:], self.board[:][start_col]) = (saved_row, saved_col) 
                raise ValueError('Please place only letters on the board')
            if self.is_scrabble_tile(curr_row, curr_col) and self.board[curr_row][curr_col] != to_place:
                (self.board[start_row][:], self.board[:][start_col]) = (saved_row, saved_col) 
                raise ValueError('Your tile {0} overlaps existing tiles on the board (perhaps from a concurrent session?)'.format(to_place))
            #remove from rack and place if this isn't an existing tile on the board
            if self.board[curr_row][curr_col] != to_place:
                self.board[curr_row][curr_col] = to_place
                player.rack.remove(to_place)
                self.board_to_player[curr_row][curr_col] = player.name #stamp tile with this player's name
    self.num_words_placed += 1
    
#http://www.csc.kth.se/utbildning/kth/kurser/DD143X/dkand12/Group3Johan/report/berntsson_ericsson_report.pdf example scoring
#calculate score--compute score for a given word off of the "real" board to calculate bonsues
    #hence this does not affect the shadow board, nor does it touch the real board aside from pulling bonuses
    #this allows us to abstract out the calc score function for computing both crosswords and regular words,
    #and allows ut to correctly compute bonuses for overlapping crosswords and regular words
#valid_crossword_score_dict is a cache of the crossword scores for that spot
    #if it is empty, then there are no crosswords to compute
    #hence, when pull_valid_crossword_score calls this function, it passes an empty dictionary
#we ask for the word and calculate scores based on this (instead of walking over the board) 
    #because this allows us to remember bonuses (ehhh not really...you could always undo)                           
def calc_word_score(self, start_row, start_col, direction, word, valid_crossword_score_dict):
    
    num_tiles = len(word) #to set boundaries
    num_tiles_used = 0 #to keep track of bingo score
                           
    crossword_scores = 0 #to keep track of ALL crossword scores
    total_score = 0 #running total score
    word_multiplier = 1 #overall word multiplier
    letter_multiplier = 1 #individual tile multipliers
    
    #set boundaries
    if direction == HORIZONTAL:
        end_row = start_row + 1
        end_col = start_col + num_tiles
    else:
        end_row = start_row + num_tiles
        end_col = start_col + 1
                           
    #increment over the word while checking the bonus values on the real board (NO PLACEMENT IS DONE)                  
    for curr_row in range(start_row, end_row):
        for curr_col in range(start_col, end_col):
            #if we aren't overlapping an existing tile, then increment the tile count
            if not self.is_scrabble_tile(curr_row, curr_col):
                num_tiles_used = num_tiles_used + 1
            
            #calculate score and bonus for this letter
            curr_letter = word[curr_row - start_row + curr_col - start_col]
            curr_bonus = self.board[curr_row][curr_col]
            
            if curr_bonus == TRIPLE_LETTER:
                letter_multiplier = 3
            elif curr_bonus == DOUBLE_LETTER:
                letter_multiplier = 2
            elif curr_bonus == TRIPLE_WORD:
                word_multiplier *= 3
            elif curr_bonus == DOUBLE_WORD:
                word_multiplier *= 2
            else:
                curr_bonus = NO_BONUS #technically includes letter tiles--can remove this when printing is no longer done
                           
            total_score += letter_multiplier * self.scrabble_score_dict[curr_letter]
            letter_multiplier = 1
    
            #add in crossword score
            if valid_crossword_score_dict:
                if (curr_row, curr_col) in valid_crossword_score_dict.keys():
                    #this letter should always exist as a key since we precalculated all crossword combinations
                    crossword_scores += valid_crossword_score_dict[(curr_row, curr_col)][curr_letter]                  
            #http://blog.lerner.co.il/calculating-scrabble-scores-reduce/ 
            #reduce(lambda total, current: total + points[current], word, 0)
            
            #TBD printing for debugging
            if valid_crossword_score_dict and DEBUG_PULL_VALID_CROSSWORD:
                print(str(curr_letter) + ": " + str(self.scrabble_score_dict[curr_letter]) + "pts" + \
                  " --> bonus : " + str(curr_bonus) + " pts at " + str(curr_row) + "," + str(curr_col))                                  
            elif DEBUG_PULL_VALID_CROSSWORD:
                print("\t" + str(curr_letter) + ": " + str(self.scrabble_score_dict[curr_letter]) + "pts" + \
                  " --> bonus : " + str(curr_bonus) + " pts at " + str(curr_row) + "," + str(curr_col))                                  
            
    #final word multiplier bonus
    total_score *= word_multiplier
    if not valid_crossword_score_dict and DEBUG_PULL_VALID_CROSSWORD:
        print("Word multiplier: " + str(word_multiplier) + " --> Total score: " + str(total_score) + " pts")
    elif DEBUG_PULL_VALID_CROSSWORD:
        print("\tWord multiplier: " + str(word_multiplier) + " --> Total score: " + str(total_score) + " pts")
    
    #add in crossword scores and bingo scores
    total_score += crossword_scores
    if valid_crossword_score_dict and num_tiles_used == RACK_MAX_NUM_TILES:
        total_score += BINGO_BONUS
        if DEBUG_PULL_VALID_CROSSWORD:
            print("Bingo bonus of: " + str(BINGO_BONUS) + " pts")
    
    if DEBUG_PULL_VALID_CROSSWORD:
        print("Final score: " + str(total_score) + " pts")
    return total_score


#this is called once we hit the end of a word     
def computer_save_word_and_score(self, curr_offset, hook_row, hook_col, direction, word, valid_crossword_score_dict, indent):
    (start_row, start_col, end_row, end_col) = self.find_coordinate_bounds_of_word(curr_offset, hook_row, hook_col, direction, word)
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

        
#checks if there is a valid crossword orthogonal to the original tile
#returns a score of -1 if there the input letter creates an invalid crossword, 
#a score of 0 if there is no crossword (so any tile is OK)
#and a 1+ score if there is a valid crossword
def pull_valid_crossword_score(self, orig_letter, orig_row, orig_col, orig_direction):
    #saved_tile = self.board[orig_row][orig_col]
    #self.board[orig_row][orig_col] = orig_letter
                           
    #if not self.is_scrabble_tile(self.shadow_board, orig_row, orig_col):
    #    raise ValueError('Attempted to calculate crossword at a non-letter tile: ' + 
    #                    str(self.shadow_board[orig_row][orig_col]) + " " + str(orig_row) + ", " + str(orig_col))
    #crossword.append(self.board[orig_row][orig_col])
    #if a tile already exists there, we do not need to check crosswords--
    #--because this tile has already been placed, and its crossword validated/scored in a previous move
    if self.is_scrabble_tile(orig_row, orig_col):
        crossword_score = -1
        if DEBUG_PULL_VALID_CROSSWORD:
            print("Existing tile already; no need to calculate crossword")
        return crossword_score
    crossword = []
    crossword.append(orig_letter)

    #first find the beginning of the word
    (curr_row, curr_col) = (orig_row, orig_col)
    if orig_direction == HORIZONTAL:
        (row_delta, col_delta) = (-1, 0)
    else:
        (row_delta, col_delta) = (0, -1)
    while True:
        (curr_row, curr_col) = (curr_row + row_delta, curr_col + col_delta)
        if curr_row >= MIN_ROW and curr_col >= MIN_COL and self.is_scrabble_tile(curr_row, curr_col):
            crossword.insert(0, self.board[curr_row][curr_col]) #insert in front
        else:
            break
            
    #save the beginning row/col
    crossword_start_row = curr_row - row_delta #undo the most recent delta operation that caused the loop break
    crossword_start_col = curr_col - col_delta
    
    #reset and find the end of the word
    (curr_row, curr_col) = (orig_row, orig_col)
    (row_delta, col_delta) = (row_delta * -1, col_delta * -1)
    while True:
        (curr_row, curr_col) = (curr_row + row_delta, curr_col + col_delta)
        if curr_row < MAX_ROW and curr_col < MAX_COL and self.is_scrabble_tile(curr_row, curr_col):
            crossword.append(self.board[curr_row][curr_col]) #append to end
        else:
            break  
    
    #TBD: better method...
    #crossword = ''.join([letter.strip() for letter in crossword_list])
    if DEBUG_PULL_VALID_CROSSWORD:
        print(crossword)
    #no crosswords were formed, so it is ok to place this tile here
    if len(crossword) == 1:
        crossword_score = 0 
    #we formed a valid crossword-->calculate the score!
    elif self.is_valid_word(crossword):
        if DEBUG_PULL_VALID_CROSSWORD:
            print("\tCrossword is: " + str(crossword) + " located at " + str(crossword_start_row) + ", " + str(crossword_start_col))
        crossword_score = self.calc_word_score (crossword_start_row, crossword_start_col, \
                                                      -1 * orig_direction, crossword, {})
    #we formed an invalid crossword
    else:
        crossword_score = -1  
    
    if DEBUG_PULL_VALID_CROSSWORD:
        print("\tCrossword score is: " + str(crossword_score) + " pts")
    return crossword_score
        
def pull_spot_to_valid_crossword_score(self, orig_row, orig_col, orig_direction, \
                                        valid_crossword_score_dict, rack):
    #saved_shadow_tile = self.shadow_board[orig_row][orig_col]
    #dedupe the rack since we shouldn't compute the score for the same letter twice
    rack_uniq = set(rack)
    #TBD: if blank, then just compute all alphabetic letters
    for letter in rack_uniq:
        #self.shadow_board[orig_row][orig_col] = letter
        crossword_score = self.pull_valid_crossword_score(letter, orig_row, orig_col, orig_direction)
        #score of negative one means crossword is invalid
        if crossword_score != -1:
            if (orig_row, orig_col) in valid_crossword_score_dict.keys():
                if letter in valid_crossword_score_dict.keys():
                    raise ValueError("Found a duplicate in crossword score dict")
                valid_crossword_score_dict[(orig_row, orig_col)][letter] = crossword_score
            else:
                valid_crossword_score_dict[(orig_row, orig_col)] = {}
                valid_crossword_score_dict[(orig_row, orig_col)][letter] = crossword_score
                
def pull_valid_hook_spot(self, row, col, valid_hook_spots):
    #if this is the first word placed on the board, it must start left of or above of the center spot
    if self.num_words_placed == 0:
        if row <= CENTER_ROW and col <= CENTER_COL:
            valid_hook_spots.append((row, col))
    #check if this is a blank spot 
    elif not self.is_scrabble_tile(row, col):
        #check if there is a non-blank spot on the board adjacent to it
        #TBD: is_scrabble_tile returns false if we go out of bounds...
        if self.is_scrabble_tile(row - 1, col) or \
        self.is_scrabble_tile(row + 1, col) or \
        self.is_scrabble_tile(row, col - 1) or \
        self.is_scrabble_tile(row, col + 1):                          
            valid_hook_spots.append((row, col))   
            #elif self.is_scrabble_tile(self.board, curr_row, curr_col) and \
            #((orig_direction == HORIZONTAL and self.is_empty_tile(self.board, curr_row, curr_col + 1)) or \
            #(orig_direction == VERTICAL and self.is_empty_tile(self.board, curr_row + 1, curr_col))):
            #    valid_starting_hook_spots.extend((curr_row, curr_col))

#given a direction (horizontal or vertical) and rack of tiles, 
#this function finds all "hook"/anchor spots that we can place words at
#this function also creates a mapping from each spot in that row/col to all valid crosswords
    #these are the crosswords orthogonal to the desired direction 
    #(e.g. I want to place horizontally-->which words allow for valid vertical crosswords?)
def pull_hooks(self, start_row, start_col, direction, rack):
    if direction == HORIZONTAL:
        (end_row, end_col) = (start_row + 1, MAX_COL)
    else:
        (end_row, end_col) = (MAX_ROW, start_col + 1)
    
    valid_hook_spots = []
    for row in range(start_row, end_row):
        for col in range(start_col, end_col):
            self.pull_valid_hook_spot(row, col, valid_hook_spots)              

    return valid_hook_spots
    
def pull_crosswords(self, start_row, start_col, direction, rack):
    if direction == HORIZONTAL:
        (end_row, end_col) = (start_row + 1, MAX_COL)
    else:
        (end_row, end_col) = (MAX_ROW, start_col + 1)
    
    valid_crossword_score_dict = {} 
    for row in range(start_row, end_row):
        for col in range(start_col, end_col):
             self.pull_spot_to_valid_crossword_score(row, col, direction, valid_crossword_score_dict, rack)  

    return valid_crossword_score_dict
    
    
#####
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
#tries to concatenate the input letter onto the prefix or suffix of the word    
def concatenate_next(self, letter, curr_node, curr_rack, curr_word,
                   curr_offset, hook_row, hook_col, direction, boundary,
                   valid_crossword_score_dict, indent):
    #if we've reached an ending node, save this word (for both prefix and suffix b/c the prefix could be the WHOLE word)
    if letter in curr_node.eow_set:
        if curr_offset <= 0:
            completed_word = [letter] + curr_word
        else:
            completed_word = curr_word + [letter]
        if not self.ends_are_filled(curr_offset, hook_row, hook_col, direction, completed_word, FRONT_OR_BACK_END):
            if DEBUG_GENERATE_MOVES:
                print(indent + "reached an eow: " + str(completed_word))
            self.computer_save_word_and_score(curr_offset, hook_row, hook_col, direction, completed_word, 
                                       valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT) 
    #placing prefix
    if curr_offset <= 0:
        if letter in curr_node.edges.keys():
            curr_node = curr_node.edges[letter]
            new_word = [letter] + curr_word
            if DEBUG_GENERATE_MOVES:
                print(indent + "building up prefix: " + str(new_word) + " with rack " + str(curr_rack))
            self.generate_moves_for_hook_spot(curr_node, curr_rack, new_word,
                                curr_offset - 1, hook_row, hook_col, direction, boundary,
                                valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT)
            #if the next node leads to a hook, then we have to reverse 
            #(unless we're bumping up against another tile on the board)
            if scrabble_apprentice_gaddag.GADDAG_HOOK in curr_node.edges.keys() and \
            not self.ends_are_filled(curr_offset, hook_row, hook_col, direction, new_word, FRONT_END):
                curr_node = curr_node.edges[scrabble_apprentice_gaddag.GADDAG_HOOK]
                if DEBUG_GENERATE_MOVES:
                    print(indent + "found a hook-->reversing now with: " + str(new_word) + " with rack " + str(curr_rack))
                self.generate_moves_for_hook_spot(curr_node, curr_rack, new_word,
                                1, hook_row, hook_col, direction, boundary,
                                valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT)
        elif DEBUG_GENERATE_MOVES:
            print (indent + "unable to continue building prefix")
    #placing suffix
    else:      
        if letter in curr_node.edges.keys():
            curr_node = curr_node.edges[letter]
            new_word = curr_word + [letter]
            
            if DEBUG_GENERATE_MOVES:
                print(indent + "building up suffix: " + str(new_word))
            self.generate_moves_for_hook_spot(curr_node, curr_rack, new_word,
                                curr_offset + 1, hook_row, hook_col, direction, boundary,
                                valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT)
        elif DEBUG_GENERATE_MOVES:
            print (indent + "unable to continue building suffix")
            
            
            
#####
        
def is_valid_word(self, word):
    return "".join(word) in self.scrabble_corpus 
    
        
        
        
    
#####
def draw_tiles_end_of_turn(self, player, num_tiles):
    self.draw_from_scrabble_bag(player, num_tiles)
    
#exchange up to the # of tiles remaining in the bag (the first n tiles in tiles_to_exchange are used)
def exchange_tiles_during_turn_capped(self, player, tiles_to_exchange):
    tiles_left_in_bag = len(self.board.bag)
    print(tiles_left_in_bag)
    print("exchange_tiles_during_turn_capped: tiles_to_exchange {0}, tiles_left_in_bag {1}".format(tiles_to_exchange, tiles_left_in_bag))
    if tiles_left_in_bag == 0:
        raise ValueError("Nothing can be exchanged because no tiles are left in the bag")
    if len(tiles_to_exchange) > tiles_left_in_bag:
        print("truncating") 
        self.exchange_tiles_during_turn(player, tiles_to_exchange[0:tiles_left_in_bag])
    else:
        print("regular")
        self.exchange_tiles_during_turn(player, tiles_to_exchange)
        
def exchange_tiles_during_turn(self, player, tiles_to_exchange):
    if len(tiles_to_exchange) == 0:
        raise ValueError("You must exchange at least 1 tile")
    self.draw_from_scrabble_bag(player, len(tiles_to_exchange), tiles_to_exchange)
         
def draw_from_scrabble_bag(self, player, num_tiles_to_draw, tiles_to_exchange = None):
    if tiles_to_exchange and num_tiles_to_draw != len(tiles_to_exchange):
        raise ValueError("Don't cheat. You're trying to draw more tiles than you are exchanging")
    
    print("num_tiles_to_draw: {0}, tiles_to_exchange: {1}".format(num_tiles_to_draw, str(tiles_to_exchange)))
    if num_tiles_to_draw < 1 or num_tiles_to_draw > RACK_MAX_NUM_TILES:
        raise ValueError("You must {0} between 1 and {1} tiles".format("exchange" if tiles_to_exchange else "draw", RACK_MAX_NUM_TILES))
    
    num_tiles_left = len(self.board.bag) 
    if num_tiles_to_draw > num_tiles_left and tiles_to_exchange:
        raise ValueError("Not enough tiles left in the bag for you to exchange {0} tiles".format(num_tiles_to_draw))
    num_tiles_to_draw = min(num_tiles_to_draw, num_tiles_left) 
    
         
    #if exchanging tiles, first remove these from rack and append back to the bag 
    if tiles_to_exchange:
        #create a copy first to validate that all requested tiles can actually be exchanged
        new_rack = player.rack[:]
        new_bag = self.board.bag[:]
        for tile in tiles_to_exchange:
            try:
                new_rack.remove(tile)
                new_bag.append(tile)
                print(tile + " added back to bag")
            except:
                print("Attempted to exchange tiles that are not in your rack. Don't cheat")
                return
        player.rack = new_rack[:]
        self.board.bag = new_bag[:]
        random.shuffle(self.board.bag)
    
    #now draw to fill back up the player's rack    
    for i in range(0, num_tiles_to_draw):
        letter = random.choice(self.board.bag)
        self.board.bag.remove(letter)
        player.rack.append(letter)
        print("Drew tile {0}".format(letter))
         
