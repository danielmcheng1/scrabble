
import sys 

import tile  
import location    
import board 
import rack 
import gaddag 
import game_controller 

# REFACTOR tiles are not deep copied 
# REFACTOR errors? at least not value error....
class Move: 
    PLACE_TILES = "Place tiles"
    EXCHANGE_TILES = "Exchange tiles"
    PASS = "Pass"
    MADE_ILLEGAL_MOVE = "Made illegal move"
    STARTED_GAME = "Started game"
    HORIZONTAL = 1
    VERTICAL = -1
    PREFIX_OFFSET = -1
    SUFFIX_OFFSET = 1
    BINGO_BONUS = 50
    
    def __init__(self, board, bag, player, action = None, tiles = None):
        # save hook spots and crossword spots -- used to determine validity throughout 
        self.all_hook_spots = self.pull_all_hook_spots(board)
        self.all_crossword_scores = self.pull_all_crossword_scores(board, player.rack)
        print("Human" if player.is_human() else "Computer")
        print(player.rack.serialize()
         
        # logs (1) if the human's attempted move was valid, and (2) the optimal move calculated by the computer 
        # game controller class uses this to update the board/racks and return to the front end 
        self.result = {"player": player, "action": action, "success": False, "detail": {}, "error": ""}
        # need to initiate Move, but not play when starting the game controller class 
        if action == Move.STARTED_GAME:
            return
        # now attempt the move 
        if player.is_human:
            self.attempt_human_move(board, bag, player, action, tiles)
        else:
            self.attempt_computer_move(board, bag, player) 
            
    '''
    FOR HUMAN PLAYER:
        (1) Validate that attempted move is legal (e.g. tiles placed on board form a valid word, exchanging a valid # of tiles)
        (2) If the player is attempting to place tiles on the board, pull the full word (since this involves board tiles) and calculate the score 
    '''
    def attempt_human_move(self, board, bag, player, move_type, attempted_tiles):
        if move_type == Move.PLACE_TILES:
            sorted_tiles = self.sort_tiles(attempted_tiles)
            self.attempt_place_tiles(sorted_tiles, board)
        elif move_type == Move.EXCHANGE_TILES:
            self.attempt_move_exchange_tiles(attempted_tiles, bag)
        elif move_type == Move.PASS:
            self.attempt_move_pass()
        
    ### HUMAN: PLACE TILES ###
    def attempt_place_tiles(self, sorted_tiles, board):
        try:
            self.validate_nonzero_tiles(sorted_tiles)
            self.validate_in_one_row_or_column(sorted_tiles)
            self.validate_tiles_hook_onto_existing(sorted_tiles)
        except Exception as e:
            self.log_error_human(e)
            return 
         
        direction = self.get_direction(sorted_tiles) 
        start_location = self.find_start_of_word(sorted_tiles[0].location, direction, board)
        num_tiles = len(sorted_tiles) 
        
        # now walk down from the start location and pull the entire sequence of tiles forming the word (= tiles on board + tiles placed by player) 
        current_location = start_location
        tile_index = 0 
        tile_word = [] 
        while True:
            # existing board tile 
            if board.has_tile(current_location):
                tile_word.append(board.get_tile(current_location)) 
            # we've used all the tiles placed by the player 
            elif tile_index == num_tiles:
                break  
            # player did not place anything here 
            elif sorted_tiles[tile_index].location != current_location:
                self.log_error_human("Placed tiles must be connected to each other") 
                return 
            # player placed a tile here 
            else:
                try:
                    self.validate_valid_crossword_formed(current_location, direction, sorted_tiles[tile_index].letter)
                except Exception as e:
                    self.log_error_human(e)
                    return 
                tile_word.append(sorted_tiles[tile_index]) 
                tile_index += 1
                
            # now increment to the next spot 
            if direction == Move.HORIZONTAL:
                current_location = current_location.offset(0, 1)
            else:
                current_location = current_location.offset(1, 0)
        
        # validate the full word now that we've walked down the board 
        try:
            self.validate_tile_word_in_dictionary(tile_word)
        except Exception as e:
            self.log_error_human(e)
            return 
        
        # score and log the result 
        score = self.calc_word_score(tile_word, board)
        self.log_success_human_placed(tile_word, sorted_tiles, score)
        
    ### VALIDATE PLACING TILES FOR HUMAN ###
    def validate_tile_word_in_dictionary(self, tile_word):
        self.validate_word_in_dictionary([tile.letter for tile in tile_word])
        
    def validate_word_in_dictionary(self, word):
        letter_representation = "".join(word)
        if letter_representation not in gaddag.SCRABBLE_CORPUS:
            raise ValueError("{0} is not a valid word in the {1}".format(letter_representation, gaddag.SCRABBLE_CORPUS_NAME))
        
    def validate_nonzero_tiles(self, tiles):
        if len(tiles) == 0:
            raise ValueError("You must place at least one tile. If you cannot move, exchange tiles or simply pass")
        
    def validate_in_one_row_or_column(self, tiles):
        (used_rows, used_cols) = self.find_used_rows_and_cols(tiles)
        if len(used_rows) != 1 and len(used_cols) != 1:
            raise ValueError("You can only place in one row or column")    
        
    def validate_tiles_hook_onto_existing(self, tiles):
        intersection = set(self.all_hook_spots).intersection([tile.location.get_tuple() for tile in tiles])
        if len(intersection) == 0:
            raise ValueError("Your placed tiles must hook onto an existing tile on the board")
            
    def validate_valid_crossword_formed(self, location, direction, letter):
        if direction == Move.HORIZONTAL:
            cross_direction_description = "vertically"
        else:
            cross_direction_description = "horizontally"
        (row, col) = location.get_tuple()
        if letter not in self.all_crossword_scores[direction][(row, col)].keys():
            raise ValueError("Your placed tile {0} fails to form a valid crossword going {1}".format(letter, cross_direction_description))
       
    ### OTHER SUPPORTING METHODS FOR HUMAN PLACING TILES ###
    def sort_tiles(self, tiles):
        return sorted(tiles, key = lambda tile: (tile.location.get_row(), tile.location.get_col()))
    
    def get_direction(self, sorted_tiles):
        (used_rows, used_cols) = self.find_used_rows_and_cols(sorted_tiles)
        if len(used_rows) == 1:
            # exception: if only one tile is placed, check if the word formed is actually going Move.VERTICALly 
            if len(used_cols) == 0 and self.has_tile_above_or_below(sorted_tiles[0], board):
                direction = Move.VERTICAL 
            else:
                direction = Move.HORIZONTAL 
        else: 
            direction = Move.VERTICAL 
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
        start_location = location_of_first_placed_tile 
        while board.has_tile(start_location):
            if direction == Move.HORIZONTAL:
                start_location = start_location.offset(-1, 0)
            else:
                start_location = start_location.offset(0, -1)
        return start_location
    
    
    ### HUMAN EXCHANGING TILES ###
    def attempt_move_exchange_tiles(self, tiles, bag):
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
    
    ### HUMAN MOVE: PASSING ###
    def attempt_move_pass(self):
        self.log_success_move_passed()
        
        
    ''' 
    COMPUTER MOVE:
        (1) Run greedy algorithm to find the highest scoring word on this turn 
        (2) If no moves are possible, log that the computer exchanged all tiles in rack 
        (3) If no tiles are left, log that the computer passed 
    '''
    def attempt_computer_move(self, board, bag, player):        
        self.find_highest_scoring_word(board, player.rack)
        if not self.result["success"]:
            if bag.has_tiles_left():
                num_tiles_to_exchange = min(bag.num_tiles_left(), rack.Rack.MAX_NUM_TILES)
                self.log_success_exchanged(player.rack.get_n_tiles(num_tiles_to_exchange))
            else:
                self.log_success_move_passed()
                

    ### COMPUTER FINDING HIGHEST SCORING MOVE ###
    def find_highest_scoring_word(self, board, rack):
        for (hook_row, hook_col) in self.all_hook_spots:
            self.find_all_words_at_hook_location(board, rack, location.Location(hook_row, hook_col))
        
    def find_all_words_at_hook_location(self, board, rack, hook_location):
        # First find all Move.HORIZONTAL words 
        path_on_board = Move.Path(self, board, hook_location, hook_location, Move.HORIZONTAL, Move.PREFIX_OFFSET)
        tile_builder = Move.TileBuilder(rack, [], [])
        self.build_words(game_controller.SCRABBLE_GADDAG.start_node, path_on_board, tile_builder)
        
        # Then find all Move.VERTICAL words 
        path_on_board = Move.Path(self, board, hook_location, hook_location, Move.VERTICAL, Move.PREFIX_OFFSET)
        tile_builder = Move.TileBuilder(rack, [], [])
        self.build_words(game_controller.SCRABBLE_GADDAG.start_node, path_on_board, tile_builder)
        
   
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
                    # print"Computer found a word picking up a board tile: {0} onto {1}".format(letter, "".join([tile.letter for tile in tile_builder.tile_word])))
                    for tile in tile_builder.tile_word:
                        pass # printtile.serialize())
                    new_tile_builder = tile_builder.use_tile_on_board(curr_tile, path)
                    score = self.calc_word_score(new_tile_builder.tile_word, path.board)
                    self.log_success_computer_placed(new_tile_builder.tile_word, new_tile_builder.tiles_used, score)
                '''else:
                    if not curr_tile.letter == letter:
                        # print"Did not complete word, board tile conflicted with {0}!".format(letter))
                    else:
                        # print"Did not complete word, board tile matched but path had no room for letter {0}!".format(letter))
                    for tile in tile_builder.tile_word:
                        # print"  {0}".format(tile.serialize()))'''
            else:
                if path.letter_in_all_crossword_scores(letter) and tile_builder.rack_has_letter(letter) and path.has_room():
                    # print"Computer found a word picking up a rack tile: {0} onto {1}".format(letter, "".join([tile.letter for tile in tile_builder.tile_word])))
                    for tile in tile_builder.tile_word:
                        pass # printtile.serialize())
                    new_tile_builder = tile_builder.use_tile_in_rack(letter, path)
                    score = self.calc_word_score(new_tile_builder.tile_word, path.board)
                    self.log_success_computer_placed(new_tile_builder.tile_word, new_tile_builder.tiles_used, score)
                '''else:
                    if not path.letter_in_all_crossword_scores(letter):
                        # print"Did not complete word, {0} not in all crossword scores".format(letter))
                    elif not tile_builder.rack_has_letter(letter):
                        # print"Did not complete word, {0} not in rack".format(letter))
                    else:
                        # print"Did not complete word, rack and crossword matched but path did not have room for {0}".format(letter))
                    for tile in tile_builder.tile_word:
                        # print"  {0}".format(tile.serialize()))'''
        # now recurse on for all other edges going out from this node
        for letter in node.edges.keys():
            # check if we need to reverse from prefix formation to suffix formation 
            if letter == gaddag.GADDAG_HOOK:
                # before starting the suffix, check that there are no tiles before the first tile in our word (which would imply this is not actually the first tile) 
                if path.has_room():
                    new_path = path.switch_to_suffix()
                    self.build_words(node.edges[letter], new_path, tile_builder) 
            
            # now try to use a tile already on the board
            elif path.has_board_tile():
                curr_tile = path.get_board_tile()
                if curr_tile.letter == letter:
                    new_tile_builder = tile_builder.use_tile_on_board(curr_tile, path)
                    new_path = path.move_one_square()
                    self.build_words(node.edges[letter], new_path, new_tile_builder) 
            
            # otherwise, try to use a tile from the rack, constrained by it forming a valid crossword 
            else:
                if path.letter_in_all_crossword_scores(letter) and tile_builder.rack_has_letter(letter):
                    new_tile_builder = tile_builder.use_tile_in_rack(letter, path)
                    new_board_path = path.move_one_square()
                    self.build_words(node.edges[letter], new_board_path, new_tile_builder) 
                    
                    
    class Path:
        # direction = {Move.HORIZONTAL, Move.VERTICAL} -- i.e. should I navigate along the row or along the columns 
        # offset = {Move.PREFIX_OFFSET, Move.SUFFIX_OFFSET} -- i.e. am I moving left/up (building up the prefix) or right/down (building up the suffix) 
        def __init__(self, move, board, hook_location, curr_location, direction, offset):
            self.move = move 
            self.board = board 
            self.hook_location = hook_location 
            self.curr_location = curr_location 
            self.direction = direction 
            self.offset = offset
        def __str__(self):
            return "@{location}, offset {offset}, going {direction} from {hook}".format(direction = self.direction, hook = self.hook_location, location = self.curr_location, offset = self.offset)
        ### READ FUNCTIONS (nothing modified so no new path is returned) ###
        def has_board_tile(self):
            return self.board.has_tile(self.curr_location)
            
        def get_board_tile(self):
            return self.board.get_tile(self.curr_location) 
        
        # REFACTOR: this is the only way to allow access between Path class and all_crossword_scores = instance variable in Move class 
        def letter_in_all_crossword_scores(self, letter):
            (row, col) = self.curr_location.get_tuple()
            return letter in self.move.all_crossword_scores[self.direction][(row, col)].keys()   
            
        ### BOUNDARY CHECKS ###
        # check if we've moved passed the board boundaries
        def outside_board(self):
            (row, col) = self.curr_location.get_tuple()
            return row < self.board.MIN_ROW or row >= self.board.MAX_ROW or col < self.board.MIN_COL or col >= self.board.MAX_COL 
            
        # checks if we have room (= no tile on the board)--if we were to continue offsetting in the current direction 
        def has_room(self):
            if self.direction == Move.HORIZONTAL:
                return not self.board.has_tile(self.curr_location.offset(0, self.offset))
            else: 
                return not self.board.has_tile(self.curr_location.offset(self.offset, 0))
        
        # checks if we hit a PREVIOUS hook spot; hence the offset must be going left/up (Move.PREFIX_OFFSET) 
        def hit_previous_hook_spot(self):
            return self.curr_location != self.hook_location and self.offset == Move.PREFIX_OFFSET and self.curr_location.get_tuple() in self.move.all_hook_spots
        
        
         ### WRITE FUNCTIONS (path needs to be modified so return a new instance) 
        def switch_to_suffix(self):
            if self.offset != Move.PREFIX_OFFSET:
                raise ValueError("Can only swith to suffix state from prefix state")
            if self.direction == Move.HORIZONTAL:
                return Move.Path(self.move, self.board, self.hook_location, self.hook_location.offset(0, 1), self.direction, Move.SUFFIX_OFFSET)
            else:
                return Move.Path(self.move, self.board, self.hook_location, self.hook_location.offset(1, 0), self.direction, Move.SUFFIX_OFFSET)
         
        def move_one_square(self):
            if self.direction == Move.HORIZONTAL:
                return Move.Path(self.move, self.board, self.hook_location, self.curr_location.offset(0, self.offset), self.direction, self.offset)
            else:
                return Move.Path(self.move, self.board, self.hook_location, self.curr_location.offset(self.offset, 0), self.direction, self.offset)
        
    class TileBuilder:
        def __init__(self, rack, tile_word, tiles_used):
            self.rack = rack.copy_rack()
            self.tile_word = [tile.copy_tile() for tile in tile_word[:]]
            self.tiles_used = [tile.copy_tile() for tile in tiles_used[:]]
        def __str__(self):
            return "rack : {0}, tile_word: {1}, tiles_used: {2}".format(self.rack.serialize(), self.concatenate_tiles(self.tile_word), self.concatenate_tiles(self.tiles_used))
        
        def concatenate_tiles(self, tiles):
            return "".join([tile.letter for tile in tiles])
            
        def rack_has_letter(self, letter):
            return self.rack.contains_letter(letter)
           
        def use_tile_in_rack(self, letter, path):
            # tile is moved from rack and "placed" on the board (temporarily) 
            new_rack = self.rack.copy_rack()
            removed_tile = new_rack.use_one_tile_with_letter(letter)
            removed_tile.change_location(path.curr_location)
            
            # offset determines if we are adding to the prefix or suffix 
            if path.offset == Move.PREFIX_OFFSET:
                return Move.TileBuilder(new_rack, [removed_tile] + self.tile_word, [removed_tile] + self.tiles_used) 
            else:
                return Move.TileBuilder(new_rack, self.tile_word + [removed_tile], self.tiles_used + [removed_tile]) 
            
        def use_tile_on_board(self, tile, path):
            # offset determines if we are adding to the prefix or suffix 
            if path.offset == Move.PREFIX_OFFSET:
                return Move.TileBuilder(self.rack, [tile] + self.tile_word, self.tiles_used)
            else:
                return Move.TileBuilder(self.rack, self.tile_word + [tile], self.tiles_used)
        
        
    '''
    SHARED METHODS BETWEEN COMPUTER AND HUMAN
    '''
    ### HOOK SPOT GENERATION ###
    # hook spots: list of (row, col) where a new word could be placed
    def pull_all_hook_spots(self, local_board):
        valid_hook_spots = []
        for row in range(board.Board.MIN_ROW, board.Board.MAX_ROW):
            for col in range(board.Board.MIN_COL, board.Board.MAX_COL):
                if self.is_valid_hook_spot(local_board, location.Location(row, col)):
                    valid_hook_spots.append((row, col))
                    
        return valid_hook_spots
    
    def is_valid_hook_spot(self, local_board, location):
        if local_board.num_words_placed == 0: 
            if location.get_row() == board.Board.CENTER_ROW and location.get_col() == board.Board.CENTER_COL:
                return True 
            return False 
        else:
            if local_board.has_tile(location):
                return False 
            else:
                #check if there is a non-blank spot on the board adjacent to it
                if local_board.has_tile(location.offset(-1, 0)) or local_board.has_tile(location.offset(1, 0)):
                    return True 
                if local_board.has_tile(location.offset(0, -1)) or local_board.has_tile(location.offset(0, 1)):
                    return True 
                return False 
                    
    ### CROSSWORD GENERATION ###
    # crossword score dicts (one for Move.HORIZONTAL, one for Move.VERTICAL): 
        # keys = (row, col)
        # values = dictionary of letters 
            # keys = valid letter for that location 
            # values = score for that crossword  
    def pull_all_crossword_scores(self, local_board, rack):
        print("pull_all_crossword_scores")
        
        crossword_scores_for_move_horizontal = {}
        crossword_scores_for_move_vertical = {}
        for row in range(board.Board.MIN_ROW, board.Board.MAX_ROW):
            for col in range(board.Board.MIN_COL, board.Board.MAX_COL):
                curr_location = location.Location(row, col)
                crossword_scores_for_move_horizontal[(row, col)] = self.pull_crossword_scores_at_location(local_board, curr_location, Move.HORIZONTAL, rack) 
                crossword_scores_for_move_vertical[(row, col)] = self.pull_crossword_scores_at_location(local_board, curr_location, Move.VERTICAL, rack) 
        return {Move.HORIZONTAL: crossword_scores_for_move_horizontal, Move.VERTICAL: crossword_scores_for_move_vertical}

    def pull_crossword_scores_at_location(self, board, location, orig_direction, rack):
        #dedupe the rack so we only compute crossword  scores for minimum set of letters 
        letters_to_score = {}
        for letter in rack.get_letter_set():
            #score of negative one means crossword is invalid
            crossword_score = self.pull_crossword_score_for_letter(board, letter, location, orig_direction)
            if crossword_score != -1:
                letters_to_score[letter] = crossword_score 
        return letters_to_score 

    # checks if there is a valid crossword orthogonal to the original tile
        # returns a score of -1 if the input letter creates an invalid crossword, 
        # a score of 0 if there is no crossword (so any tile is OK)
        # and a 1+ score if there is a valid crossword
    def pull_crossword_score_for_letter(self, board, letter, location, orig_direction):
        # if a tile already exists there, no crosswords can be placed here 
        if board.has_tile(location):
            return -1
            
        # find the start location for this crossword
        crossword_direction = orig_direction * -1
        start_location = self.find_start_of_word(location, crossword_direction, board)
        
            
        # generate the crossword 
        tile_crossword = []
        current_location = start_location
        while True:
            if board.has_tile(current_location):
                tile_crossword.append(board.get_tile(current_location))
            else:
                # create a tile for this temporary crossword letter since we finding all potential crosswords  
                if current_location == start_location:
                    tile_crossword.append(tile.Tile(letter, None, current_location))
                # no more board tiles means we've hit the end of the crossword 
                else:
                    break 
            if crossword_direction == Move.HORIZONTAL:
                current_location = current_location.offset(0, 1)
            else:
                current_location = current_location.offset(1, 0)
        #no crosswords were formed, so it is ok to place this tile here
        if len(tile_crossword) == 1:
            return 0
            
        # check if we formed a valid word 
        try:
            self.validate_tile_word_in_dictionary(tile_crossword)              
        # return if we formed an invalid crossword
        except:
            return -1
        
        # calculate the score 
        return self.calc_word_score(tile_crossword, board, False) 
        
        
    ### SCORE CALCULATION ###
    # calculate Scrabble score for a word (represented as a list of TILE objects)
    # include_crosswords flag because we only compute crossword scores for actual placement -- 
        # when using this method for caching all possible crossword scores, we do not want to calculate crossword scores for those cached crosswords
    def calc_word_score(self, tile_word, board, include_crosswords = True):
        # print"Entering calc_word_score")
        for tile in tile_word:
            pass # printtile.serialize())
            
        if len(tile_word) == 0: 
            return 0 
        direction = self.get_direction(tile_word) 
        start_location = tile_word[0].location 
        # print"start_location is " + str(start_location))
        num_tiles_placed = 0 # if 7 tiles placed, then add bingo bonus 
        crossword_scores = 0 # to keep track of all crossword scores (avoid applying multiplier twice to these)
        total_score = 0 # running total score
        word_multiplier = 1 # running word multiplier (applied at the end)

        for i in range(0, len(tile_word)):
            # print"i is " + str(i))
            # move to the next location on the board
            if direction == Move.HORIZONTAL:
                location = start_location.offset(0, i)
            else:
                location = start_location.offset(i, 0)
            # print"offseting to " + str(location))
            (row, col) = location.get_tuple()
            
            # only count multipliers for new squares (i.e. multiplier only counts at the time of play) 
            letter_multiplier = 1 
            if not board.has_tile(location):
                letter_multiplier = board.get_bonus_letter_multiplier(row, col)
                word_multiplier *= board.get_bonus_word_multiplier(row, col)
                num_tiles_placed += 1
            total_score += letter_multiplier * tile_word[i].points 
            
            # add in scores from crossword (multipliers already included in these) 
            letter = tile_word[i].letter
            if include_crosswords and letter in self.all_crossword_scores[direction][(row, col)].keys():
                crossword_scores += self.all_crossword_scores[direction][(row, col)][letter]
        
        #final word multiplier bonus
        total_score *= word_multiplier
        
        #add in crossword scores and bingo scores
        total_score += crossword_scores
        if num_tiles_placed == rack.Rack.MAX_NUM_TILES:
            total_score += Move.BINGO_BONUS
            
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
    
    def get_resulting_player(self):
        return self.result.get("player")
        
    
    ### LOGGING THE RESULT ###
    def log_error_human(self, e): 
        self.result["success"] = False 
        self.result["action"] = Move.MADE_ILLEGAL_MOVE
        if type(e) is str:
            self.result["error"] = e 
        else:
            self.result["error"] = "".join(e.args)
        
    def log_success_human_placed(self, tile_word, tiles_used, score):
        self.result["success"] = True 
        self.result["action"] = Move.PLACE_TILES
        self.result["detail"]["word"] = "".join([tile.letter for tile in tile_word])
        self.result["detail"]["tiles_used"] = tiles_used 
        self.result["detail"]["score"] = score 
        
    def log_success_computer_placed(self, tile_word, tiles_used, score):
        self.result["success"] = True 
        self.result["action"] = Move.PLACE_TILES
        
        if score > self.result["detail"].get("score", -1):
            self.result["detail"]["score"] = score 
            self.result["detail"]["word"] = "".join([tile.letter for tile in tile_word])
            self.result["detail"]["tiles_used"] = tiles_used
            
    def log_success_exchanged(self, tiles_used):
        self.result["success"] = True 
        self.result["action"] = Move.EXCHANGE_TILES
        self.result["detail"]["word"] = "EXCHANGED TILES"
        self.result["detail"]["tiles_used"] = tiles_used 
        self.result["detail"]["score"] = 0 
        
    def log_success_move_passed(self):
        self.result["success"] = True 
        self.result["action"] = Move.PASS
        self.result["detail"]["word"] = "PASSED TURN"
        self.result["detail"]["tiles_used"] = [] 
        self.result["detail"]["score"] = 0
        
        
    def serialize_result(self):
        # exception for the detail key because we have to apply nested serialization (could refactor with proper serialization for all other data elements 
        detail = {}
        for key in self.result["detail"]:
            if key == "tiles_used":
                detail["tiles_used"] = [tile.serialize() for tile in self.result["detail"]["tiles_used"]]
            else:
                detail[key] = self.result["detail"][key]
                
        return {"player": self.result["player"].serialize_type(), \
                "action": self.result["action"], \
                "success": str(self.result["success"]), \
                "detail": detail, \
                "error": self.result["error"]}
    
    # printing functions for debugging 
    PRINT_DIVIDER = "-------------------------------"
    def print_all_hook_spots(self):
        print("HOOK SPOTS", file=sys.stderr)
        for hook_spot in self.all_hook_spots:
            print(hook_spot, file=sys.stderr)
        print(Move.PRINT_DIVIDER, file=sys.stderr)
        
    def print_all_crossword_scores(self):
        print("\nPrinting all_crossword_scores")
        for direction in self.all_crossword_scores:
            for (x, y) in self.all_crossword_scores[direction]:
                print(str((x, y)) + " --> " + str(self.all_crossword_scores[direction][(x, y)]))
        print(Move.PRINT_DIVIDER)
    def print_tile_list(self, tile_list):
        # print"\nPrinting tile list")
        for tile in tile_list:
            pass # printtile.serialize()) 
        # printMove.PRINT_DIVIDER)
                        