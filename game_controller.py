
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
        self.draw_tiles_end_of_turn(player, RACK_MAX_NUM_TILES)
        self.last_move = {}
        
    def process_human_move(self, action, tiles):
        # do not process further if the game has already ended 
        if self.game_has_ended():
            return self.serialize()
        
        # validate the attempted human move
        human_move = move.Move(self.board, self.bag, self.human_player, action, tiles)
        if human_move.succeeded():
            # implement the attempted human move 
            last_move = human_move.get_result()
            self.realize_move(last_move) 
            
            # now find the optimal computer move is 
            computer_move = move.Move(self.board, self.bag, self.compute_player)
            
            # and implement that computer move 
            last_move = computer_move.get_result() 
        
        # pass the result back to the front end 
        return self.serialize()
            
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
    
 
 