

class game_controller:
        
    MIN_WORD_LENGTH = 2
    SCRABBLE_CORPUS  = load_scrabble_corpus()

    #1: Loading scrabble score and frequency dictionaries, as well as bag and entire corpurs
    #source lexicon: http://www.wordgamedictionary.com/twl06/download/twl06.txt -- the FreeScrabbleDictionary_twl06.txt, used for North American tournaments
    def load_scrabble_corpus():
        scrabble_corpus= []
        #os.pardir to go back up a level
        with open(os.path.join(os.path.dirname( __file__ ), 'static', 'data', 'FreeScrabbleDictionary_twl06.txt'), newline = '') as raw_corpus:
            for word in csv.reader(raw_corpus):
                cleaned_word = ''.join(word).upper()
                if len(cleaned_word) >= MIN_WORD_LENGTH: #this excludes 'A' and 'I'...for now...TBD
                    scrabble_corpus.extend([cleaned_word])
        return scrabble_corpus

    def __init__(self, board, 
                 scrabble_player_1, 
                 scrabble_player_2 = None,
                 scrabble_player_3 = None,
                 scrabble_player_4 = None):
        self.board = board
        self.current_player = scrabble_player_1
        self.round_num = 1 
        self.num_turns_passed = 0
        self.play_order = []
        #set the play order, and draw tiles for each player
        for player in [scrabble_player_1, scrabble_player_2, scrabble_player_3, scrabble_player_4]:
            if player:
                self.play_order.append(player)
                self.draw_tiles_end_of_turn(player, RACK_MAX_NUM_TILES)
       
    def print_game_state(self):
        print("Current Round: " + str(self.round_num))
        print("Play Order: WILL BE FINISHED")
        #+ ", ".join(self.play_order))
        print("Number of tiles left in the bag: " + str(len(scrabble_bag)))
        self.board.print_board()
        print("Current player: " + self.current_player.name)

    
        
                
    def game_has_ended(self):
        return self.game_end_reason() != ""
    
    #game ends if (1) six turns have ended in passes or (2) a player has no tiles left and there are no tiles left in the bag 
    def game_end_reason(self):
        if self.num_turns_passed == MAX_TURNS_PASSED: 
            return "Game over: {0} turns have ended in passes".format(MAX_TURNS_PASSED)
        if len(self.board.bag) == 0:
            for player in self.play_order: 
                if len(player.rack) == 0: 
                    return "Game over: {0} used up all tiles in rack, and no tiles are left in the bag".format(player.name)
        return ""
    