
import tile  
import location     
class Move: 
    PLACE_TILES = "Place tiles"
    EXCHANGE_TILES = "Exchange tiles"
    PASS = "Pass"
    MADE_ILLEGAL_MOVE = "Made illegal move"
    HORIZONTAL = 1
    VERTICAL = -1
    BINGO_BONUS = 50
    
    def __init__(self, board, bag, player, action = None, tiles = None):
        self.all_hook_spots = self.pull_all_hook_spots(board)
        self.all_crossword_scores = self.pull_all_crossword_scores(board, player)
        self.result = {"player": player, "action": action, "success_flag": False, "detail": {}}
        
        if self.player.is_human():
            self.attempt_human_move(board, bag, player, tiles)
        else:
            self.attempt_computer_move(board, bag, player) 
        
         
               
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
            self.log_error_human(e)
            return 
            
        direction = self.get_direction(sorted_tiles) 
        start_location = find_start_of_word(sorted_tiles[0].location, direction, board)
        
        # now walk down from the start location and pull the entire sequence of tiles forming the word (= tiles on board + tiles placed by player) 
        current_location = start_location
        tile_index = 0 
        tile_word = [] 
        while True:
            # existing board tile 
            if board.has_tile(location):
                tile_word.append(board.get_tile(location)) 
            # we've used all the tiles placed by the player 
            elif tile_index == num_tiles:
                break  
            # player did not place anything here 
            elif sorted_tiles[tile_index].location != location:
                self.log_error_human("Placed tiles must be connected to each other") 
                return 
            # player placed a tile here 
            else:
                try:
                    self.validate_valid_crossword_formed(location, direction, sorted_tiles[tile_index].letter)
                except as e:
                    self.log_error_human(e)
                    return 
                tile_word.append(sorted_tiles[tile_index]) 
                tile_index += 1
                
            # now increment to the next spot 
            if direction == HORIZONTAL:
                current_location = current_location.offset(-1, 0)
            else 
                current_location = current_location.offset(0, -1)
        
        # validate the full word now that we've walked down the board 
        try:
            self.validate_tile_word_in_dictionary(tile_word)
        except as e:
            self.log_error_human(e)
            return 
        self.log_success(PLACE_TILES, tile_word)
        
        
        #score and place word
        human_score = self.calc_word_score(tile_word, board)
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
    
    # walk upwards/leftwards from the first player-placed tile, until there are no more existing board tiles 
    # this must then be the start of the actual word 
    def find_start_of_word(self, location_of_first_placed_tile, direction, board):
        start_location = some_location 
        while board.has_tile(location):
            if direction == HORIZONTAL:
                start_location = start_location.offset(-1, 0)
            else 
                start_location = start_location.offset(0, -1)
        return start_location
    
    #################        
    # calculate Scrabble score for a word (represented as a list of TILE objects)
    def calc_word_score(self, tile_word, board):
        if len(tile_word) == 0: 
            return 0 
        start_location = tile_word[0].location 
            
        num_tiles_placed = 0 # if 7 tiles placed, then add bingo bonus 
        crossword_scores = 0 # to keep track of all crossword scores (avoid applying multiplier twice to these)
        total_score = 0 # running total score
        word_multiplier = 1 # running word multiplier (applied at the end)

        for i in range(0, len(tile_word)):
            # move to the next location on the board
            if direction == HORIZONTAL:
                location = start_location.offset(i, 0)
            else:
                location = start_location.offset(0, i)
            (row, col) = location.get_tuple()
            
            # only count multipliers for new squares (i.e. multiplier only counts at the time of play) 
            letter_multiplier = 1 
            if not board.has_tile(location):
                letter_multiplier = board.get_bonus_letter_multiplier(row, col)
                word_multiplier *= board.get_bonus_word_multiplier(row, col)
                num_tiles_placed += 1
            total_score += letter_multiplier * tile_word[i].points 
            
            # add in scores from crossword (multipliers already included in these) 
            if letter in all_crossword_scores[direction][(row, col)].keys():
                crossword_scores += all_crossword_scores[direction][(row, col)][letter]
        
        #final word multiplier bonus
        total_score *= word_multiplier
        
        #add in crossword scores and bingo scores
        total_score += crossword_scores
        if num_tiles_placed == rack.MAX_NUM_TILES:
            total_score += BINGO_BONUS
            
        return total_score        

        
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
    def log_error_human(e): 
        result["success_flag"] = False 
        result["action"] = MADE_ILLEGAL_MOVE
        result["detail"]["description"] = "".join(e.args)
        
    def log_success_human_placed(tile_word, tiles_used, score):
        result["success_flag"] = True 
        result["action"] = PLACE_TILES
        result["detail"]["word"] = "".join([tile.letter for tile in tile_word])
        result["detail"]["tiles_used"] = tiles_used 
        result["detail"]["score"] = score 
        
    def log_success_computer_placed(word, context):
        result["success_flag"] = True 
        result["action"] = PLACE_TILES
        tiles_used = context.tiles_used  
        word = context.word 
        score = self.calc_word_score(tiles_
        if score > result["detail"].get("score", 0):
            result["detail"]["score"] = score 
            result["detail"]["word"] = word
            result["detail"]["tiles_used"] = tiles_used 
            
                  self.location = location 
            self.generating_prefix = generating_prefix
            self.rack = rack.copy_rack()
            self.word = word[:] if word is not None else []
            self.letter = letter if letter is not None else ""
            self.node = node if node is not None else SCRABBLE_APPRENTICE_GADDAG.start_node 
            self.tiles_placed = tiles_placed[:] if tiles_placed is not None else []
         
    def log_success_exchanged(tiles_used):
        result["success_flag"] = True 
        result["action"] = EXCHANGE_TILES
        result["detail"]["word"] = "EXCHANGED"
        result["detail"]["tiles_used"] = [] 
        result["detail"]["score"] = 0 
        
    def log_success_passed():
        result["success_flag"] = True 
        result["action"] = PASS
        result["detail"]["word"] = "PASSED"
        result["detail"]["tiles_used"] = [] 
        result["detail"]["score"] = 0
        
    # returns result of attempted move by computer or human 
    # "attempted" because human tile placement may be invalid
    # game controller classes uses this to update the board/rack and return to the front end 
    def get_result(self):
        return self.result 
        
        
    def validate_tile_word_in_dictionary(self, tile_word):
        self.validate_word_in_dictionary([tile.letter for tile in tile_word])
        
    def validate_word_in_dictionary(self, word):
        letter_representation = "".join(word)
        if letter_representation not in self.scrabble_corpus:
            raise ValueError("{0} is not a valid word in the TWL06 Scrabble dictionary".format(letter_representation))
        
    def validate_nonzero_tiles(self, tiles):
        if len(tiles) == 0:
            raise ValueError("You must place at least one tile. If you cannot move, exchange tiles or simply pass")
        
    def validate_in_one_row_or_column(self, tiles):
        (used_rows, used_cols) = self.find_used_rows_and_cols(tiles)
        if len(used_rows) != 1 and len(used_cols) != 1:
            raise ValueError("You can only place in one row or column")    
        
    def validate_tiles_hook_onto_existing(self, tiles):
        intersection = set(self.all_hook_spots).intersection([tile.location.tuple() for tile in tiles])
        if len(intersection) == 0:
            raise ValueError("Your placed tiles must hook onto an existing tile on the board")
            
    def validate_valid_crossword_formed(self, location, direction, letter):
        if direction == HORIZONTAL:
            cross_direction_description == "vertically"
        else:
            cross_direction_description == "horizontally"
        (row, col) = location.get_tuple()
        if letter not in all_crossword_scores[direction][(row, col)].keys():
            raise ValueError("Your placed tile {0} fails to form a valid crossword going {1}".format(letter, cross_direction_description))
     
    #####
    ### HOOK SPOT GENERATION
    #hook spots: list of (row, col) where a new word could be placed
    def pull_all_hook_spots(self, board):
        valid_hook_spots = []
        for row in range(board.MIN_ROW, board.MAX_ROW):
            for col in range(board.MIN_COL, board.MAX_COL):
                if self.is_valid_hook_spot:
                    valid_hook_spots.append((row, col))
                    
        return valid_hook_spots
    
     def is_valid_hook_spot(self, board, location):
        (row, col) = location.get_tuple()
        if board.num_words_placed == 0:
            if row <= board.CENTER_ROW and row > board.CENTER_ROW - rack.MAX_NUM_TILES:
                return True 
            elif col <= board.CENTER_COL and col > board.CENTER_COL - rack.MAX_NUM_TILES:
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
                    
    #CROSSWORD GENERATION
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
                crossword_scores_for_horizontal[(row, col)] = pull_crossword_scores_at_location(location.Location(row, col), HORIZONTAL, rack) 
                crossword_scores_for_vertical[(row, col)] = pull_crossword_scores_at_location(location.Location(row, col), VERTICAL, rack) 
        return {HORIZONTAL: crossword_scores_for_horizontal, VERTICAL: crossword_scores_for_vertical)}

    def pull_crossword_scores_at_location(self, location, orig_direction, rack):
        #dedupe the rack so we only compute crossword  scores for minimum set of letters 
        letters_to_score = {}
        for letter in rack.get_set():
            #score of negative one means crossword is invalid
            crossword_score = self.pull_crossword_score_for_letter(letter, location, orig_direction)
            if crossword_score != -1:
                letters_to_score[letter] = crossword_score 
        return letters_to_score 

    # checks if there is a valid crossword orthogonal to the original tile
        # returns a score of -1 if the input letter creates an invalid crossword, 
        # a score of 0 if there is no crossword (so any tile is OK)
        # and a 1+ score if there is a valid crossword
    def pull_crossword_score_for_letter(self, letter, location, orig_direction):
        # if a tile already exists there, no crosswords can be placed here 
        if board.has_tile(location):
            return -1
            
        # find the start location for this crossword
        crossword_direction = orig_direction * -1
        start_location = self.find_start_of_word(location, crossword_direction, board)
        
        #no crosswords were formed, so it is ok to place this tile here
        if start_location == location:
            return 0
            
        # generate the crossword 
        tile_crossword = []
        current_location = start_location 
        while True:
            if board.has_tile(location):
                tile_crossword.append(board.get_tile(location))
            else:
                # create a tile for this temporary crossword letter since we finding all potential crosswords  
                if current_location == start_location:
                    tile_crossword.append(tile.Tile(letter, self.player, location))
                # no more board tiles means we've hit the end of the crossword 
                else:
                    break 
            if direction == HORIZONTAL:
                location = location.offset(1, 0)
            else:
                location = location.offset(0, 1)
                
        # check if we formed a valid word 
        try:
            self.validate_tile_word_in_dictionary(tile_crossword)              
        # return if we formed an invalid crossword
        except:
            return -1
        
        # calculate the score 
        return self.calc_word_score(tile_crossword, board) 
        
        
        
        
        

            
                    
    #################
    # search_context = helps build word
    # search constraint = helps search the gaddag and board, never changes  for a given call to generate_moves_for_hook_spot  
    class Context:
        def __init__(self, rack, location, generating_prefix, letter, tile_word, node, tiles_placed):
            self.location = location 
            self.generating_prefix = generating_prefix
            self.rack = rack.copy_rack()
            self.tile_word = tile_word[:] if tile_word is not None else []
            self.letter = letter if letter is not None else ""
            self.node = node if node is not None else SCRABBLE_APPRENTICE_GADDAG.start_node 
            self.tiles_placed = tiles_placed[:] if tiles_placed is not None else []
        
        def get_location_tuple(self):
            return self.location.get_tuple() 
            
        def get_word(self):
            return "".join([tile.letter for tile in self.tile_word])
            
        def rack_contains_letter(self, letter):
            return self.rack.contains_letter(letter)
            
        def rack_has_tiles_left(self):
            return self.rack.has_tiles_left()
            
            
            
        def accept_tile_on_board(self, tile):
            return Context(letter = tile.letter, self.tile_word + [tile])
            
        def remove_letter_from_rack(self, letter):
            return Context(self.rack.remove_one_tile(letter))
            
        #stop placing if we've reached the previous hook spot (or if we pass the max boundary of the board)
        def hit_boundary(self, board, constraint):
            if constraint.direction == HORIZONTAL and self.curr_col < constraint.boundary:
                return True 
            if constraint.direction == VERTICAL and self.curr_row < constraint.boundary:
                return True
            if self.curr_col >= board.MAX_COL:
                return True 
            if self.curr_row >= board.MAX_ROW:
                return True 
            return False 
            
    class Constraint:
        def __init__(self, hook_row, hook_col, direction, boundary):
            self.hook_row = hook_row 
            self.hook_col = hook_col 
            self.direction = direction 
            self.boundary = boundary 
        
    def attempt_computer_move(self, player, board):        
        self.generate_all_possible_moves(player.rack, board)
        if self.comp_max_word:
            self.place_word(self.comp_max_row, self.comp_max_col, self.comp_max_direction, self.comp_max_word, player)
        return (self.comp_max_score, self.comp_max_word)

    def generate_all_possible_moves(self, rack, board):
        # iterate over all possible hook spots, building up words going both HORIZONTALLY and VERTICALLY 
        # maintain pointer to the previous hook spot so that we do not recalculate possible words for that spot--when moving back from the current spot 
        boundary = MIN_COL
        for (hook_row, hook_col) in valid_hook_spots:
            constraint = Constraint(hook_row, hook_col, HORIZONTAL, boundary)
            context = Context(rack, Location.location(hook_row, hook_col), True, None, None, None)
            
            self.generate_moves_for_hook_spot(board, constraint, context)
            boundary = hook_col + 1
       
        boundary = MIN_ROW
        for (hook_row, hook_col) in valid_hook_spots:
            constraint = Constraint(hook_row, hook_col, VERTICAL, boundary)
            context = Context(rack, Location.location(hook_row, hook_col), True, None, None, None)
            
            self.generate_moves_for_hook_spot(board, constraint, context)
            boundary = hook_row + 1
         
    def generate_moves_for_hook_spot(self, board, constraint, context):  
        if context.hit_boundary(constraint):
            return
        
        # first try to use an existing board tile as the next letter in the word 
        if board.has_tile(context.location):     
            self.concatenate_next(board, constraint, context.accept_tile_on_board(board.get_tile(context.location)))
            return 
            
        # otherwise, see if we can tiles left in our rack 
        if not context.has_tiles_left_on_rack():
            return 
        
        # try placing any letters in our rack that also form valid crossword 
        for letter in valid_crossword_score_dict[context.get_location_tuple()].keys():
            if context.rack_contains_letter(letter):
                self.concatenate_next(board, constraint, context.remove_letter_from_rack(letter)) 
                
    #REFACTOR CORE RECURSIVE CALL -- keep building up the string 
    #tries to concatenate the input letter onto the prefix or suffix of the word    
    def process_letter_in_gaddag(self, board, constraint, context):
        #if we've reached an ending node, save this word (for both prefix and suffix b/c the prefix could be the WHOLE word)
        if context.reached_end_of_word():
            completed_word_context = context.move_letter_to_word()
            # check that there is not a tile to the left/right of our word (which would invalidate this being the beginning/end of the word )
            if completed_word_context.has_room():
                self.log_success_computer_placed(completed_word_context)
                
            if not self.ends_are_filled(curr_offset, hook_row, hook_col, direction, completed_word, FRONT_OR_BACK_END):
                self.computer_save_word_and_score(curr_offset, hook_row, hook_col, direction, completed_word, 
                                           valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT) 
        def reached_end_of_word(self):
            return self.letter in self.node.eow_set 
        def move_letter_to_word(self):
            if self.generating_prefix:
                completed_word = [self.letter] + self.word 
            else:
                completed_word = self.word + [self.letter]
            return Context(letter = "", completed_word) 
            
        def has_room(self, board, constraint, context):
            if context.generating_prefix:
                sign = -1
            else:
                sign = 1
            if constraint.direction == HORIZONTAL:
                if board.has_tile(context.location.offset(sign, 0)):
                    return False 
                else:
                    return True 
            else:
                if board.has_tile(context.location.offset(0, sign)):
                    return False 
                else:
                    return True 
                    
                    
        #placing prefix
        if curr_offset <= 0:
            if letter in curr_node.edges.keys():
                curr_node = curr_node.edges[letter]
                new_word = [letter] + curr_word
                self.generate_moves_for_hook_spot(curr_node, curr_rack, new_word,
                                    curr_offset - 1, hook_row, hook_col, direction, boundary,
                                    valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT)
                #if the next node leads to a hook, then we have to reverse 
                #(unless we're bumping up against another tile on the board)
                if scrabble_apprentice_gaddag.GADDAG_HOOK in curr_node.edges.keys() and \
                not self.ends_are_filled(curr_offset, hook_row, hook_col, direction, new_word, FRONT_END):
                    curr_node = curr_node.edges[scrabble_apprentice_gaddag.GADDAG_HOOK]
                    self.generate_moves_for_hook_spot(curr_node, curr_rack, new_word,
                                    1, hook_row, hook_col, direction, boundary,
                                    valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT)
        #placing suffix
        else:      
            if letter in curr_node.edges.keys():
                curr_node = curr_node.edges[letter]
                new_word = curr_word + [letter]
                self.generate_moves_for_hook_spot(curr_node, curr_rack, new_word,
                                    curr_offset + 1, hook_row, hook_col, direction, boundary,
                                    valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT)
                
        
        
    def find_coordinate_bounds_of_word(self, curr_offset, hook_row, hook_col, direction, word):
        if direction == HORIZONTAL:
            # either we were offset to the beginning of the word (i.e. we hit eow on a reversed prefix)
            if curr_offset <= 0:
                (start_row, start_col) = (hook_row, hook_col + curr_offset)
            # or we were offset to the end of the word
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
       
    # checks that if we continue to concatenate, that there is NOT a tile to the left (above) or to the right (below) of this eow
    def ends_are_filled(self, curr_offset, hook_row, hook_col, direction, word, front_or_back):
        (start_row, start_col, end_row, end_col) = \
            self.find_coordinate_bounds_of_word(curr_offset, hook_row, hook_col, direction, word)
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
               
                        