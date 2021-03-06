
import gaddag 
#global data structures so that this only loads once to server all requests 
SCRABBLE_GADDAG = gaddag.read_gaddag_full()

import board 
import bag
import player 

import move 
import tile 
import location 

class GameController:
    MAX_CONSECUTIVE_TURNS_PASSED = 6
    def __init__(self):
        self.board = board.Board()
        self.bag = bag.Bag()
        self.human_player = player.Player(player.Player.IS_HUMAN)
        self.computer_player = player.Player(player.Player.IS_COMPUTER)
        
        self.round_num = 1 
        self.num_consecutive_turns_passed = 0
        self.human_player.draw_tiles_at_start_of_game(self.bag)
        self.computer_player.draw_tiles_at_start_of_game(self.bag)
        
        # initiate last move to computer passing the previous round 
        self.last_move = move.Move(self.board, self.bag, self.computer_player, move.Move.STARTED_GAME)
        
    def process_human_move(self, action, tiles = None):
        # do not process further if the game has already ended 
        if self.game_has_ended():
            return self.serialize()
        
        # validate the attempted human move
        self.last_move = move.Move(self.board, self.bag, self.human_player, action, tiles)
        if self.last_move.succeeded():
            # implement the attempted human move 
            self.implement_last_move() 
            
            # now find the optimal computer move
            if 1 == 1:
                self.last_move = move.Move(self.board, self.bag, self.computer_player)
                
                # and implement that computer move 
                self.implement_last_move()
        
        # pass the result back to the front end 
        return self.serialize()
        
    def implement_last_move(self):
        last_move = self.last_move
        action = last_move.get_resulting_action()
        player = last_move.get_resulting_player()
        
        if action == move.Move.PLACE_TILES:
            player.use_tiles_for_placing(last_move.get_resulting_tiles_used())
            self.board.play_tiles(last_move.get_resulting_tiles_used())
            self.num_consecutive_turns_passed = 0
        elif action == move.Move.EXCHANGE_TILES:
            player.exchange_tiles(self.bag, last_move.get_resulting_tiles_used())
            self.num_consecutive_turns_passed = 0
        elif action == move.Move.PASS:
            self.num_consecutive_turns_passed += 1 
            
        player.add_new_word_played(last_move.get_resulting_word(), last_move.get_resulting_score())
        player.draw_tiles_at_end_of_turn(self.bag)
        
        
    # game ends if (1) six turns have ended in passes or (2) a player has no tiles left and there are no tiles left in the bag 
    def game_end_reason(self):
        if self.num_consecutive_turns_passed == GameController.MAX_CONSECUTIVE_TURNS_PASSED: 
            return "Game over: {0} turns have ended in passes".format(GameController.MAX_CONSECUTIVE_TURNS_PASSED)
        if not self.bag.has_tiles_left():
            if not self.human_player.rack.has_tiles_left(): 
                return "Game over: {0} used up all tiles in your rack, and no tiles are left in the bag".format("You")
            if not self.computer_player.rack.has_tiles_left():
                return "Game over: {0} used up all tiles in its rack, and no tiles are left in the bag".format("Computer")
        return ""
           
    def game_has_ended(self):
        return self.game_end_reason() != ""
    
    # dumping out miscellaneous info for front end view
    def serialize_game_info(self):
        game_info = {}
        game_info["scoreHuman"] = self.human_player.running_score
        game_info["scoreComputer"] = self.computer_player.running_score 
        game_info["wordsPlayedHuman"] = self.human_player.words_played
        game_info["wordsPlayedComputer"] = self.computer_player.words_played
        game_info["tilesLeft"] = self.bag.num_tiles_left()
        game_info["gameEndReason"] = self.game_end_reason()
        return game_info
 
    
    # final dump for front end (camel case for front end Javascript convention)
    def serialize(self):
        wrapper = {}
        wrapper["board"] = self.board.serialize_grid()
        wrapper["tiles"] = self.board.serialize_tiles_placed()
        wrapper["rackHuman"] = self.human_player.serialize_rack()
        wrapper["rackComputer"] = self.computer_player.serialize_rack()
        wrapper["gameInfo"] = self.serialize_game_info()
        wrapper["lastMove"] = self.last_move.serialize_result() if self.last_move is not None else {}
        return wrapper 
        
    def print_serialize(self):
        serialized = self.serialize()
        for key in serialized:
            print(key)
            if key in ("board", "tiles", "rackHuman", "rackComputer"):
                for elem in serialized[key]:
                    print(elem)
            else:
                for key_inner in serialized[key]:
                    print("  {key_inner}: {value}".format(key_inner = key_inner, value = serialized[key][key_inner]))
        print("------------------------------\n")
    
   # convert front end data to tile moves
    def front_end_json_to_tiles(self, user_json):
        print(user_json) 
        action = user_json["action"]
        tiles = []
        if action == move.Move.PLACE_TILES:
            for i, row in enumerate(user_json["data"]):
                for j, cell in enumerate(row):
                    if cell != "":
                        tiles.append(tile.Tile(cell, self.human_player, location.Location(i, j)))
        elif action == move.Move.EXCHANGE_TILES:
            for i, letter in enumerate(user_json["data"]):
                # only need letter since these will be returned to the bag 
                tiles.append(tile.Tile(letter, None, None))
        return tiles 
        
if __name__ == "__main__":
    pass
    '''
    game = GameController()
    game.print_serialize()
    
    game.human_player.rack.use_one_tile_random()
    game.human_player.rack.use_one_tile_random()
    game.human_player.rack.use_one_tile_random()
    game.human_player.rack.use_one_tile_random()
    game.human_player.rack.use_one_tile_random()
    game.human_player.rack.use_one_tile_random()
    game.human_player.rack.add_tile(tile.Tile("G", game.human_player, location.Location(7, 7)))
    game.human_player.rack.add_tile(tile.Tile("E", game.human_player, location.Location(7, 8)))
    game.human_player.rack.add_tile(tile.Tile("N", game.human_player, location.Location(7, 9)))
    game.human_player.rack.add_tile(tile.Tile("T", game.human_player, location.Location(7, 10)))
    game.human_player.rack.add_tile(tile.Tile("L", game.human_player, location.Location(7, 11)))
    game.human_player.rack.add_tile(tile.Tile("E", game.human_player, location.Location(7, 12)))
    
    game.process_human_move(move.Move.PLACE_TILES, game.human_player.rack.tiles[-6:])
    
    
    game.human_player.rack.use_one_tile_random()
    game.human_player.rack.add_tile(tile.Tile("A", game.human_player, location.Location(6, 9)))
    game.process_human_move(move.Move.PLACE_TILES, game.human_player.rack.tiles[-1:])
    game.print_serialize()    
    i = 1
    while not game.game_has_ended():   
        if i % 2:
            game.process_human_move(move.Move.PASS) 
        else:
            n = i % 6
            game.process_human_move(move.Move.EXCHANGE_TILES, game.human_player.rack.get_n_tiles(i % 6 + 1))
        game.print_serialize() 
        i += 1
    '''