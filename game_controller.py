
import gaddag 
import corpus
#global gaddag so that this only loads once to server all requests 
#REFACTOR check if memory loaded multiple times 
SCRABBLE_GADDAG = gaddag.read_gaddag_full()
SCRABBLE_MIN_WORD_LENGTH = corpus.get_min_word_length() 
SCRABBLE_CORPUS  = corpus.load_scrabble_corpus()

class GameController:
    MAX_CONSECUTIVE_TURNS_PASSED = 6
    def __init__(self):
        self.board = board.Board()
        self.human_player = player.Player(player.IS_HUMAN)
        self.computer_player = player.Player(player.IS_COMPUTER)
        
        self.round_num = 1 
        self.num_consecutive_turns_passed = 0
        self.human_player.draw_tiles_at_start_of_game()
        self.computer_player.draw_tiles_at_start_of_game()
        
        self.last_move = None
        
    def process_human_move(self, action, tiles):
        # do not process further if the game has already ended 
        if self.game_has_ended():
            return self.serialize()
        
        # validate the attempted human move
        self.last_move = move.Move(self.board, self.bag, self.human_player, action, tiles)
        if self.last_move.succeeded():
            # implement the attempted human move 
            self.implement_last_move() 
            
            # now find the optimal computer move is 
            self.last_move = move.Move(self.board, self.bag, self.compute_player)
            
            # and implement that computer move 
            self.implement_last_move()
        
        # pass the result back to the front end 
        return self.serialize()
        
    def implement_last_move(self):
        last_move = self.last_move
        action = last_move.get_resulting_action()
        player = last_move.get_resulting_player()
        
        if action == move.PLACE_TILES:
            self.board.add_tiles(last_move.get_resulting_tiles_used())
            self.num_consecutive_turns_passed = 0
        elif action == move.EXCHANGE_TILES:
            player.exchange_tiles(self.bag, last_move.get_resulting_tiles_used())
            self.num_consecutive_turns_passed = 0
        elif action == move.PASS:
            self.num_consecutive_turns_passed += 1 
            
        player.add_new_word_played(last_move.get_resulting_word(), last_move.get_resulting_score())
        player.draw_tiles_at_end_of_turn(self.bag)
        
    def serialize(self):
        self.board.serialize_grid()
        self.board.serialize_tiles()
        self.human_player.serialize_rack()
        self.computer_player.serialize_rack()
        self.last_move 
    scrabble_game_play_wrapper = {"board": [[map_cell_to_bonus_view(scrabble_board.board[row][col]) for col in range(MAX_COL)] for row in range(MAX_ROW)], \
                              "tiles": [[map_cell_to_tile_view(scrabble_board.board[row][col], map_cell_to_player_view(row, col, scrabble_board), scrabble_score_dict) for col in range(MAX_COL)] for row in range(MAX_ROW)], \
                              "rackHuman": map_rack_to_tile_view(human_player.rack, "Human", scrabble_score_dict),   \
                              "rackComputer": map_rack_to_tile_view(computer_player.rack, "Computer", scrabble_score_dict), \
                              "gameInfo": {"scoreHuman": human_player.running_score, "scoreComputer": computer_player.running_score,
                                           "wordsPlayedHuman": human_player.words_played, "wordsPlayedComputer": computer_player.words_played,
                                           "tilesLeft": len(scrabble_board.bag),
                                           "gameEndReason": scrabble_game_play.game_end_reason()}, \
                              "lastMove": last_move_to_send
                              }
                                      
        def wrapper_end_turn(player, word, score, game_play):
            player.words_played.append({"word": word, "score": score})
            player.running_score += score   
            game_play.draw_tiles_end_of_turn(player, RACK_MAX_NUM_TILES - len(player.rack)) 
            
        def increment_turns_passed(scrabble_game_play, move):
            if move["action"] == "Passed":
                scrabble_game_play.num_turns_passed += 1
            else:
                scrabble_game_play.num_turns_passed = 0 
    def get_game_info():
        round_num
        scores by player 
        words played by player 
        count_tiles_left
        last move
        game end reason
        "gameInfo": {"scoreHuman": human_player.running_score, "scoreComputer": computer_player.running_score,
                                   "wordsPlayedHuman": human_player.words_played, "wordsPlayedComputer": computer_player.words_played,
                                   "tilesLeft": len(scrabble_board.bag),
                                   "gameEndReason": scrabble_game_play.game_end_reason()}
    
    def game_has_ended(self):
        return self.game_end_reason() != ""
    
    #game ends if (1) six turns have ended in passes or (2) a player has no tiles left and there are no tiles left in the bag 
    def game_end_reason(self):
        if self.num_consecutive_turns_passed == MAX_CONSECUTIVE_TURNS_PASSED: 
            return "Game over: {0} turns have ended in passes".format(MAX_CONSECUTIVE_TURNS_PASSED)
        if len(self.board.bag) == 0:
            if len(self.human_player.rack) == 0: 
                return "Game over: {0} used up all tiles in your rack, and no tiles are left in the bag".format("You")
            if len(self.computer_player.rack) == 0:
                return "Game over: {0} used up all tiles in its rack, and no tiles are left in the bag".format("Computer")
        return ""
    
 
 