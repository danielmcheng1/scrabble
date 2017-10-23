
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
    
    ### BAG CLASS 
    
    def draw_tiles_end_of_turn(self, player, num_tiles):
        self.draw_from_scrabble_bag(player, num_tiles)
               
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
             
                    
                            
    #exchange up to the # of tiles remaining in the bag (the first n tiles in tiles_to_exchange are used)
    def exchange_tiles_during_turn_capped(self, player, tiles_to_exchange):
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
             
 
 