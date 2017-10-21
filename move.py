
        
        
    def is_valid_word(self, word):
        return "".join(word) in self.scrabble_corpus 
        
    def play_move(self, player):
        self.print_game_state()
        player.print_player_state()
        
        if player.is_human:
            num_attempts = 0
            while True:
                (input_row, input_col, input_dir, input_word) = self.request_human_move(player)
                if input_word:
                    try:
                        score = self.board.make_human_move(input_row, input_col, input_dir, input_word, player)
                        break
                    except:
                        print("Made Illegal Move. Let's try again.")
                        num_attempts += 1
                        if num_attempts == MAX_NUM_ATTEMPTED_MOVES:
                            print("You fail at entering moves on a Scrabble board. Your turn will be skipped.")
                            break
                else:
                    player.print_player_state()
                    return
        else:
            print("Computer thinking through move....")
            (score, input_word) = self.board.make_computer_move(player)
            #if the computer is unable to find a move, exchange tiles
            if not input_word:
                self.exchange_tiles_during_turn(player, player.rack)
                

        player.words_played.append((input_word, score))
        player.running_score += score   
        self.draw_tiles_end_of_turn(player, RACK_MAX_NUM_TILES - len(player.rack)) 
        player.print_player_state()
        
        
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