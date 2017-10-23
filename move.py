
import tile  
import location    
import board 

# REFACTOR errors? at least not value error....
class Move: 
    PLACE_TILES = "Place tiles"
    EXCHANGE_TILES = "Exchange tiles"
    PASS = "Pass"
    MADE_ILLEGAL_MOVE = "Made illegal move"
    HORIZONTAL = 1
    VERTICAL = -1
    PREFIX_OFFSET = -1
    SUFFIX_OFFSET = 1
    BINGO_BONUS = 50
    
    def __init__(self, board, bag, player, action = None, tiles = None):
        # save hook spots and crossword spots -- used to determine validity throughout 
        self.all_hook_spots = self.pull_all_hook_spots(board)
        self.all_crossword_scores = self.pull_all_crossword_scores(board, player)
        
        # logs (1) if the human's attempted move was valid, and (2) the optimal move calculated by the computer 
        # game controller class uses this to update the board/racks and return to the front end 
        self.result = {"player": player, "action": action, "success": False, "detail": {}, "error": ""}
        
        # now attempt the move 
        if self.player.is_human():
            self.attempt_human_move(board, bag, player, action, tiles)
        else:
            self.attempt_computer_move(board, bag, player) 
            
    '''
    FOR HUMAN PLAYER:
        (1) Validate that attempted move is legal (e.g. tiles placed on board form a valid word, exchanging a valid # of tiles)
        (2) If the player is attempting to place tiles on the board, pull the full word (since this involves board tiles) and calculate the score 
    '''
    def attempt_human_move(self, board, bag, player, attempted_tiles, move_type):
        sorted_tiles = self.sort_tiles(attempted_tiles)
        if move_type == PLACE_TILES:
            self.attempt_place_tiles(sorted_tiles)
        elif move_type == EXCHANGE_TILES:
            self.attempt_exchange_tiles(sorted_tiles)
        elif move_type == PASS:
            self.attempt_pass()
        
    ### HUMAN: PLACE TILES ###
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
        
        # score and log the result 
        human_score = self.calc_word_score(tile_word, board)
        self.log_success_human_placed(tile_word, sorted_tiles, score)
        
    ### VALIDATE PLACING TILES FOR HUMAN ###
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
       
    ### OTHER SUPPORTING METHODS FOR HUMAN PLACING TILES ###
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
    
    
    ### HUMAN EXCHANGING TILES ###
    def attempt_exchange_tiles(self, player, tiles, bag):
        num_tiles_exchange = len(tiles) 
        num_tiles_in_bag = bag.num_tiles_left() 
        exchange_grammar = "tile" if num_tiles_exchange == 1 else "tiles" 
        bag_grammar = "tile" if num_tiles_in_bag == 1 else "tiles" 
        
        if num_tiles_exchange == 0:
            self.log_error_human("Must exchange at least one tile. Perhaps you meant to pass instead?")
            return 
            
        if num_tiles_exchange > num_tiles_in_bag:
            self.log_error_human("You cannot exchange {0} {1}--only {2} {3} are left in the bag".format(num_tiles_exchange, exchange_grammar, num_tiles_in_bag, bag_grammar))
            return
        self.log_success_exchanged(tiles)
    
    ### HUMAN PASSING ###
    def attempt_pass(self, player):
        self.log_success_passed()
        
        
    ''' 
    COMPUTER MOVE:
        (1) Run greedy algorithm to find the highest scoring word on this turn 
        (2) If no moves are possible, log that the computer exchanged all tiles in rack 
        (3) If no tiles are left, log that the computer passed 
    '''
    def attempt_computer_move(self, player, board, bag):        
        self.find_highest_scoring_word(player.rack, board)
        if not self.result["success"]:
            if bag.has_tiles_left():
                log_success_exchanged(player.rack.get_n_tiles(min(bag.num_tiles_left(), rack.Rack.MAX_NUM_TILES))):
            else:
                log_success_passed()
                

    ### COMPUTER FINDING HIGHEST SCORING MOVE ###
    def find_highest_scoring_word(self, board, rack):
        for (hook_row, hook_col) in valid_hook_spots:
            self.find_all_words_at_hook_location(board, rack, location.Location(hook_row, hook_col))
    
    def find_all_words_at_hook_location(self, board, rack, hook_location):
        # First find all horizontal words 
        path_on_board = Path(board, hook_location, hook_location, HORIZONTAL, PREFIX_OFFSET)
        tile_builder = TileBuilder(rack, [], [])
        self.build_words(SCRABBLE_GADDAG.start_node, path_on_board, tile_builder)
        
        # Then find all vertical words 
        path_on_board = Path(board, hook_location, hook_location, VERTICAL, PREFIX_OFFSET)
        tile_builder = TileBuilder(rack, [], [])
        self.build_words(SCRABBLE_GADDAG.start_node, path_on_board, tile_builder)
    
    # Recursively build up words by walking down the gaddag and board
    def build_words(self, node, path, tile_builder):
        if path.hit_previous_hook_spot() or path.outside_board():
            return 
            
        curr_location = path.curr_location
        # first check if we've completed a word 
        for letter in node.eow_set:
            if path.has_board_tile():
                curr_tile = path.get_board_tile()
                if curr_tile.letter == letter and path.has_room():
                    new_tile_builder = tile_builder.add_tile(curr_tile)
                    log_success_computer_placed(new_tile_builder)
            else:
                (row, col) = curr_location.get_tuple() 
                if letter in all_crossword_scores[(row, col)].keys() and tile_builder.rack_has_letter(letter) and path.has_room():
                    new_tile_builder = tile_builder.use_tile_in_rack(letter)
                    log_success_computer_placed(new_tile_builder)
                    
        # now recurse on for all other edges going out from this node
        for letter in node.edges.keys():
            # check if we need to reverse from prefix formation to suffix formation 
            if letter === gaddag.GADDAG_HOOK:
                # before starting the suffix, check that there are no tiles before the first tile in our word (which would imply this is not actually the first tile) 
                if path.has_room():
                    new_path = path.switch_to_suffix()
                    self.get_words(node.edges[letter], new_path, tile_builder) 
            
            # now try to use a tile already on the board
            elif path.has_board_tile():
                curr_tile = path.get_board_tile()
                if curr_tile.letter == letter:
                    new_tile_builder = tile_builder.add_tile(curr_tile)
                    new_path = path.move_one_square()
                    self.get_words(node.edges[letter], new_path, new_tile_builder) 
            
            # otherwise, try to use a tile from the rack, constrained by it forming a valid crossword 
            else:
                (row, col) = curr_location.get_tuple() 
                if letter in all_crossword_scores[(row, col)].keys() and tile_builder.rack_has_letter(letter):
                    new_tile_builder = tile_builder.use_tile_in_rack(letter)
                    new_board_path = board_path.move_one_square()
                    self.get_words(node.edges[letter], new_board_path, new_tile_builder) 
                    
                    
    class Path:
        # direction = {HORIZONTAL, VERTICAL} -- i.e. should I navigate along the row or along the columns 
        # offset = {PREFIX_OFFSET, SUFFIX_OFFSET} -- i.e. am I moving left/up (building up the prefix) or right/down (building up the suffix) 
        def __init__(self, board, hook_location, curr_location, direction, offset):
            self.board = board 
            self.hook_location = hook_location 
            self.curr_location = curr_location 
            self.direction = direction 
            self.offset = offset 
            
        ### READ FUNCTIONS (nothing modified so no new path is returned) ###
        def has_board_tile(self):
            return board.has_tile(self.curr_location)
            
        def get_board_tile(self):
            return board.get_tile(self.curr_location) 
        
        def rack_has_letter(self, letter):
            return self.rack.contains_letter(letter) 
            
        # only if we hit a PREVIOUS hook spot; hence the offset must be going left/up (PREFIX_OFFSET) 
        def hit_previous_hook_spot(self):
            return curr_location != hook_location and offset == PREFIX_OFFSET and curr_location.get_tuple() in all_hook_spots
        
        # check if we've passed the board boundaries
        def outside_board(self):
            (row, col) = curr_location.get_tuple()
            return row < board.MIN_ROW or row >= board.MAX_ROW or col < board.MIN_COL or col >= board.MAX_COL 
            
        # checks if we have room (= no tile on the board)--if we were to continue offsetting in the current direction 
        def has_room(self):
            if self.direction == HORIZONTAL:
                return self.board.has_tile(self.curr_location.offset(offset, 0))
            else: 
                return self.board.has_tile(self.curr_location.offset(0, offset))

         ### WRITE FUNCTIONS (path needs to be modified so return a new instance) 
        def switch_to_suffix(self):
            if self.offset != PREFIX_OFFSET:
                raise ValueError("Can only swith to suffix state from prefix state")
            if self.direction == HORIZONTAL:
                return Path(self.board, self.hook_location, self.hook_location.offset(1, 0), self.direction, SUFFIX_OFFSET)
            else:
                return Path(self.board, self.hook_location, self.hook_location.offset(0, 1), self.direction, SUFFIX_OFFSET)
         
        def move_one_square(self):
            if self.direction == HORIZONTAL:
                return Path(self.board, self.hook_location, self.hook_location.offset(offset, 0), self.direction, self.offset)
            else:
                return Path(self.board, self.hook_location, self.hook_location.offset(0, offset), self.direction, self.offset)
                
    class TileBuilder:
        def __init__(self, rack, tile_word, tiles_used):
            self.rack = rack.copy_rack()
            self.tile_word = tile_word[:]
            self.tiles_used = tiles_used[:]
            
        def rack_has_letter(self, letter):
            return self.rack.contains_letter(letter)
            
        def use_tile_in_rack(self, letter):
            new_rack = self.rack.copy_rack()
            removed_tile = new_rack.remove_one_tile(letter)
            
            new_tile_word = self.tile_word + [removed_tile]
            new_tiles_used = self.tiles_used + [removed_tile]
            return TileBuilder(new_rack, new_tile_word, new_tiles_used) 
            
        def add_tile(self, tile):
            return TileBuilder(self.rack, self.tile_word + [tile], self.tiles_used + [tile])
        
               
    '''
    SHARED METHODS BETWEEN COMPUTER AND HUMAN
    '''
    ### HOOK SPOT GENERATION ###
    # hook spots: list of (row, col) where a new word could be placed
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
                    
    ### CROSSWORD GENERATION ###
    # crossword score dicts (one for horizontal, one for vertical): 
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
        
        
    ### SCORE CALCULATION ###
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

    ### RETRIEVING THE RESULT ###
    # REFACTOR: Is a dictionary the best data structure? .get methods hide this implementation so this can change if needed 
    def get_result(self):
        return self.result 
        
    def succeeded(self):
        return self.result.get("success", False)
        
    def get_resulting_action(self):
        return self.result.get("action", "")
    
    def get_resulting_word(self):
        return self.result.get("detail", {}).get("word", "")
    
    def get_resulting_tiles_used(self):
        return self.result.get("detail", {}).get("tiles_used", [])
    
    def get_resulting_score(self):
        return self.result.get("detail", {}).get("score", 0)
    
    def get_reuslting_player(self):
        return self.result.get("player")
        
    
    ### LOGGING THE RESULT ###
    def log_error_human(self, e): 
        result["success"] = False 
        result["action"] = MADE_ILLEGAL_MOVE
        result["error"] = "".join(e.args)
        
    def log_success_human_placed(self, tile_word, tiles_used, score):
        result["success"] = True 
        result["action"] = PLACE_TILES
        result["detail"]["word"] = "".join([tile.letter for tile in tile_word])
        result["detail"]["tiles_used"] = tiles_used 
        result["detail"]["score"] = score 
        
    def log_success_computer_placed(self, word, tile_builder):
        result["success"] = True 
        result["action"] = PLACE_TILES
        
        tiles_used = tile_builder.tiles_used
        score = self.calc_word_score(tiles_used)
        word = [tile.letter for tile in tiles_used]
        
        if score > result["detail"].get("score", 0):
            result["detail"]["score"] = score 
            result["detail"]["word"] = word
            result["detail"]["tiles_used"] = tiles_used
         
    def log_success_exchanged(self, tiles_used):
        result["success"] = True 
        result["action"] = EXCHANGE_TILES
        result["detail"]["word"] = "EXCHANGED"
        result["detail"]["tiles_used"] = [] 
        result["detail"]["score"] = 0 
        
    def log_success_passed(self):
        result["success"] = True 
        result["action"] = PASS
        result["detail"]["word"] = "PASSED"
        result["detail"]["tiles_used"] = [] 
        result["detail"]["score"] = 0
        
        
    def serialize_result(self):
        return {"player": self.result[player].serialize_type(), \
                "action": self.result[action], \
                "success": str(self.result["success"]), \
                "detail": self.result[detail], \
                "error": self.result[error]}
                
        
                        