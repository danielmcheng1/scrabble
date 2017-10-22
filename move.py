

    
class Move: 
    PLACE_TILES = "Place tiles"
    EXCHANGE_TILES = "Exchange tiles"
    PASS = "Pass"
    HORIZONTAL = 1
    VERTICAL = -1
    RACK_MAX_NUM_TILES = 7
    
    def __init__(self, board, bag, player, attempted_tiles = None, move_type = None):
        self.all_hook_spots = self.pull_all_hook_spots(board)
        self.all_crossword_scores = self.pull_all_crossword_scores(board, player)
        
        if self.player.is_human():
            self.attempt_human_move(board, bag, player, attempted_tiles)
        else:
            self.attempt_computer_move(board, bag, player) 
        
        self.comp_max_score = 0
        self.comp_max_word = []
        self.comp_max_row = None
        self.comp_max_col = None
        self.comp_max_direction = None
        self.comp_all_possible_moves = {HORIZONTAL:{}, VERTICAL:{}}
         
    # returns result of attempted move by computer or human 
    # "attempted" because human tile placement may be invalid
    # game controller classes uses this to update the board/rack and return to the front end 
    def get_move(self):
        result = {}
        result["player"] = self.player 
        result["action"] = "FINISHED MOVE"
        result["detail"] = "SCRABBLE"
        result["success"] = True 
               
    #################
    def attempt_computer_move(self, board, bag, player):
        
    def attempt_human_move(self, board, bag, player, attempted_tiles, move_type):
        sorted_tiles = self.sort_tiles(attempted_tiles)
        if move_type == PLACE_TILES:
            self.attempt_place_tiles(sorted_tiles)
        elif move_type == EXCHANGE_TILES:
            self.attempt_exchange_tiles(sorted_tiles)
        elif move_type == PASS:
            self.attempt_pass()
        
    def attempt_place_tiles(self, sorted_tiles, board):
        try:
            self.validate_nonzero_tiles(sorted_tiles)
            self.validate_in_one_row_or_column(sorted_tiles)
            self.validate_tiles_hook_onto_existing(sorted_tiles)
        except as e:
            self.log_error(e)
            return 
            
        direction = self.get_direction(sorted_tiles) 
        start_location = find_start_of_word(sorted_tiles[0].location, direction, board)
        
        # pull the whole word from existing board tiles + tiles placed by player 
        current_location = start_location
        tile_index = 0 
        word = [] 
        while True:
            # existing board tile 
            if board.has_tile(location):
                word.append(board.get_tile(location)) 
            # we've used all the tiles placed by the player 
            elif tile_index == num_tiles:
                break  
            # player did not place anything here 
            elif sorted_tiles[tile_index].location != location:
                self.log_error("Placed tiles must be connected to each other") 
                return 
            # player placed a tile here 
            else:
                try:
                    self.validate_valid_crossword_formed(location, direction, sorted_tiles[tile_index].letter)
                except as e:
                    self.log_error(e)
                    return 
                word.append(sorted_tiles[tile_index]) 
                tile_index += 1
                
            # now increment to the next spot 
            if direction == HORIZONTAL:
                current_location = current_location.offset(-1, 0)
            else 
                current_location = current_location.offset(0, -1)
        
        # validate the full word now that we've walked down  the board 
        try:
            self.validate_tileword_in_dictionary(word)
        except as e:
            self.log_error(e)
        
        self.log_success(PLACE_TILES)
        
        
        #score and place word
        human_score = self.calc_word_score(start_row, start_col, direction, word, valid_crossword_score_dict)
        return human_score
        
    # REFACTOR errors? at least not value error....
      
    def find_used_rows_and_cols(self, tiles):
        rows = set([])
        cols = set([])
        for tile in tiles:
            rows.add(tile.location.get_row())
            cols.add(tile.location.get_col())
        return (rows, cols) 
        
    def has_tile_above_or_below(self, tile, board):
        tile_row = tile.location.get_row()
        tile_col = tile.location.get_col() 
        return board.has_scrabble_tile(tile_row, tile_col - 1) or board.has_scrabble_tile(tile_row, tile_col + 1)
    
    def find_start_of_word(self, some_location, direction, board):
        start_location = some_location 
        while board.has_tile(location):
            if direction == HORIZONTAL:
                start_location = start_location.offset(-1, 0)
            else 
                start_location = start_location.offset(0, -1)
        return start_location
    
        
        
    #################
    def attempt_computer_move(self, player):        
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
        if self.has_scrabble_tile(curr_row, curr_col):
            letter = self.board[curr_row][curr_col]
            if curr_node is None:
                curr_node = SCRABBLE_APPRENTICE_GADDAG.start_node
            self.concatenate_next(letter, curr_node, curr_rack, curr_word,
                       curr_offset, hook_row, hook_col, direction, boundary,
                       valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT + GEN_MOVES_PRINT_INDENT)

        #otheriwse, if we still have tiles left, try to place
        elif curr_rack:
            #iterate over the set of valid crossletters
            if (curr_row, curr_col) in valid_crossword_score_dict.keys():
                for letter in valid_crossword_score_dict[(curr_row, curr_col)].keys():
                    if letter in curr_rack:
                        new_rack = curr_rack[:]
                        new_rack.remove(letter)
                        if DEBUG_GENERATE_MOVES:
                            print(indent + GEN_MOVES_PRINT_INDENT + "found letter " + letter + "--new rack is " + str(new_rack))
                        if curr_node is None:
                            curr_node = SCRABBLE_APPRENTICE_GADDAG.start_node
                        self.concatenate_next(letter, curr_node, new_rack, curr_word,
                                   curr_offset, hook_row, hook_col, direction, boundary,
                                   valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT + GEN_MOVES_PRINT_INDENT)
        
        
    #################        
    #http://www.csc.kth.se/utbildning/kth/kurser/DD143X/dkand12/Group3Johan/report/berntsson_ericsson_report.pdf example scoring
    def calc_word_score(self, start_location, direction, word, board):
        num_tiles_placed = 0 #to keep track of bingo score
                               
        crossword_scores = 0 #to keep track of ALL crossword scores
        total_score = 0 #running total score
        word_multiplier = 1 #overall word multiplier

        for i in range(0, len(word)):
            if direction == HORIZONTAL:
                location = start_location.offset(i, 0)
            else 
                location = start_location.offset(0, i)
                
            #if we aren't overlapping an existing tile, then increment the tile count
            if board.has_tile(location):
                letter_multiplier = board.get_bonus_letter_multiplier(location.get_row(), location.get_col())
                word_multiplier *= board.get_bonus_word_multiplier(location.get_row(), location.get_col())
            else:
                letter_multiplier = board.get_bonus_letter_multiplier(location.get_row(), location.get_col())
                word_multiplier *= board.get_bonus_word_multiplier(location.get_row(), location.get_col())
                num_tiles_placed += 1
                       
        total_score += letter_multiplier * self.scrabble_score_dict[curr_letter]
        letter_multiplier = 1

        #add in crossword score
        if valid_crossword_score_dict:
            if (curr_row, curr_col) in valid_crossword_score_dict.keys():
                #this letter should always exist as a key since we precalculated all crossword combinations
                crossword_scores += valid_crossword_score_dict[(curr_row, curr_col)][curr_letter]                  
                
        #set boundaries
        (start_row, start_col) = start_location.get_tuple() 
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
                if not board.has_scrabble_tile(curr_row, curr_col):
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
        return total_score


    #this is called once we hit the end of a word     
    def computer_save_word_and_score(self, curr_offset, hook_row, hook_col, direction, word, valid_crossword_score_dict):
        (start_row, start_col, end_row, end_col) = self.find_coordinate_bounds_of_word(curr_offset, hook_row, hook_col, direction, word)
        word_score = self.calc_word_score(start_row, start_col, direction, word, valid_crossword_score_dict)
        #exception for the first move
        if self.num_words_placed == 0 and not self.intersect_center_tile(start_row, start_col, direction, word):
            return
        
            
        cleaned_word = ''.join(word) #make this a string for ease of reading--this dictionary isn't used for anything aside from debugging
        if (start_row, start_col) in self.comp_all_possible_moves[direction].keys():
            if cleaned_word in self.comp_all_possible_moves[direction][(start_row, start_col)].keys():
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
            return self.has_scrabble_tile(front_row, front_col)
        elif front_or_back == FRONT_OR_BACK_END:
            return self.has_scrabble_tile(front_row, front_col) or self.has_scrabble_tile(back_row, back_col)
        else:
            raise ValueError("Requested something besides FRONT_END or FRONT_OR_BACK_END")
    #REFACTOR CORE RECURSIVE CALL -- keep building up the string 
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
             
 
    #####
    ### UTILITY METHODS 
    def sort_tiles(self, tiles):
        return sorted(tiles, key = lambda tile: (tile.location.get_row(), tile.location.get_col()))
    
    def get_direction(self, sorted_tiles):
        (used_rows, used_cols) = self.find_used_rows_and_cols(sorted_tiles)
        if len(filled_rows) == 1:
            # exception: if only one tile is placed, check if the word formed is actually going vertically 
            if len(sorted_tiles) == 0 and self.has_tile_above_or_below(sorted_tiles[0], board):
                direction = VERTICAL 
            else:
                direction = HORIZONTAL 
        else: 
            direction = VERTICAL 
        return direction 
        
    #####
    ### VALIDATION 
    def log_error(e):
        last_move_to_send["player"] = "Human"
        last_move_to_send["action"] = "Made Illegal Move" 
        last_move_to_send["detail"] = "".join(e.args)

    def validate_tileword_in_dictionary(self, tiles):
        self.validate_word_in_dictionary([tile.letter for tile in word])
        
    def validate_word_in_dictionary(self, word):
        letter_representation = "".join(word)
        if letter_representation not in self.scrabble_corpus:
            raise ValueError("{0} is not a valid word in the TWL06 Scrabble dictionary".format(letter_representation))
        
    def validate_nonzero_tiles(self, sorted_tiles):
        if len(sorted_tiles) == 0:
            raise ValueError("You must place at least one tile. If you cannot move, exchange tiles or simply pass")
        
    def validate_in_one_row_or_column(self, sorted_tiles):
        (used_rows, used_cols) = self.find_used_rows_and_cols(sorted_tiles)
        if len(used_rows) != 1 and len(used_cols) != 1:
            raise ValueError("You can only place in one row or column")    
        
    def validate_tiles_hook_onto_existing(self, sorted_tiles):
        intersection = set(self.all_hook_spots).intersection([tile.location.tuple() for tile in sorted_tiles])
        if len(intersection) == 0:
            raise ValueError("Your placed tiles must hook onto an existing tile on the board")
            
    def validate_valid_crossword_formed(self, location, direction, letter):
        if direction == HORIZONTAL:
            cross_direction_description == "vertically"
        else:
            cross_direction_description == "horizontally"
        (row, col) = location.get_tuple()
        if (row, col) not in all_crossword_scores.keys():
            raise ValueError("Your placed tile {0} fails to form a valid crossword going {1}".format(letter, cross_direction_description))
        if letter not in valid_crossword_score_dict[(row, col)].keys():
            raise ValueError("Your placed tile {0} fails to form a valid crossword going {1}".format(letter, cross_direction_description))
     
    #####
    ### HOOKS AND CROSSWORD GENERATION 
    #hook spots: list of (row, col) where a new word could be placed
    def pull_all_hook_spots(self, board):
        valid_hook_spots = []
        for row in range(board.MIN_ROW, board.MAX_ROW):
            for col in range(board.MIN_COL, board.MAX_COL):
                if self.is_valid_hook_spot:
                    valid_hook_spots.append((row, col))
                    
        return valid_hook_spots
    
    #crossword score dicts (one for horizontal, one for vertical): 
        # keys = (row, col)
        # values = dictionary of letters 
            # keys = valid letter for that location 
            # values = score for that crossword  
    def pull_all_crossword_scores(self, board, rack):
        crossword_scores_for_horizontal = {}
        crossword_scores_for_vertical = {}
        for row in range(board.MIN_ROW, board.MAX_ROW):
            for col in range(board.MIN_COL, board.MAX_COL):
                crossword_scores_for_horizontal[(row, col)] = pull_crossword_scores_at_location(row, col, HORIZONTAL, rack) 
                crossword_scores_for_vertical[(row, col)] = pull_crossword_scores_at_location(row, col, VERTICAL, rack) 
        return (crossword_scores_for_horizontal, crossword_scores_for_vertical) 

     def is_valid_hook_spot(self, board, location):
        (row, col) = location.get_tuple()
        if board.num_words_placed == 0:
            if row <= board.CENTER_ROW and row > board.CENTER_ROW - RACK_MAX_NUM_TILES:
                return True 
            elif col <= board.CENTER_COL and col > board.CENTER_COL - RACK_MAX_NUM_TILES:
                return True 
            else:
                return False 
        else:
            if board.has_tile(location):
                return False 
            else:
                #check if there is a non-blank spot on the board adjacent to it
                if board.has_tile(location.offset(-1, 0)) or \
                board.has_tile(location.offset(1, 0)) or 
                board.has_tile(location.offset(0, -1)) or 
                board.has_tile(location.offset(0, 1)):
                    return True 
                else:
                    return False 
                    
    
    def pull_crossword_scores_at_location(self, orig_row, orig_col, orig_direction, rack):
        #dedupe the rack so we only compute score for minimum set of letters 
        rack_uniq = set(rack)
        letters_to_score = {}
        for letter in rack_uniq:
            #score of negative one means crossword is invalid
            crossword_score = self.pull_crossword_score_for_letter(letter, orig_row, orig_col, orig_direction)
            if crossword_score != -1:
                letters_to_score[letter] = crossword_score 
        return letters_to_score 

    # checks if there is a valid crossword orthogonal to the original tile
        # returns a score of -1 if the input letter creates an invalid crossword, 
        # a score of 0 if there is no crossword (so any tile is OK)
        # and a 1+ score if there is a valid crossword
    def pull_crossword_score_for_letter(self, orig_letter, orig_row, orig_col, orig_direction):
        #if a tile already exists there, we do not need to check crosswords, because this must have been scored already in a previous move
        if self.has_scrabble_tile(orig_row, orig_col):
            crossword_score = -1
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
            if curr_row >= MIN_ROW and curr_col >= MIN_COL and self.has_scrabble_tile(curr_row, curr_col):
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
            if curr_row < MAX_ROW and curr_col < MAX_COL and self.has_scrabble_tile(curr_row, curr_col):
                crossword.append(self.board[curr_row][curr_col]) #append to end
            else:
                break  
        
        #no crosswords were formed, so it is ok to place this tile here
        if len(crossword) == 1:
            crossword_score = 0 
        #we formed a valid crossword-->calculate the score!
        elif self.is_valid_word(crossword):
            crossword_score = self.calc_word_score (crossword_start_row, crossword_start_col, \
                                                          -1 * orig_direction, crossword, {})
        #we formed an invalid crossword
        else:
            crossword_score = -1  
        
        return crossword_score
                        