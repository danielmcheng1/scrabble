
import rack 
class Player:
    IS_HUMAN = True 
    IS_COMPUTER = False 
    def __init__(self, is_human):
        self.is_human = is_human
        self.rack = rack.Rack([])  
        self.running_score = 0
        self.words_played = []      
    
    def draw_tiles_at_start_of_game(self, bag):
        self.draw_tiles(bag, rack.Rack.MAX_NUM_TILES)
        
    def draw_tiles_at_end_of_turn(self, bag):
        self.draw_tiles(bag, rack.Rack.MAX_NUM_TILES - self.rack.get_num_tiles())
        
    def draw_tiles(self, bag, n):
        # architecture assumes validation happened in move class 
        num_tiles_to_draw = min(bag.num_tiles_left(), n)
        bag.shuffle_bag()
        for i in range(0, num_tiles_to_draw):
            self.rack.add_tile(bag.draw_tile().change_player(self))
            
    def exchange_tiles(self, bag, tiles):
        bag.shuffle_bag() 
        exchanged_tiles = []
        for tile in tiles:
            exchanged_tile = self.rack.remove_one_tile_with_letter(tile.letter)
            exchanged_tiles.append(exchanged_tile.remove_player())
            
            self.rack.add_tile(bag.draw_tile().change_player(self))
        
        # remove these after drawing complete so that we don't draw a tile that we just exchanged  
        for tile in exchanged_tiles:
            bag.add_tile(tile)
    
    def add_new_word_played(self, word, score):
        self.words_played.append({"word": word, "score": score})
        self.running_score += score 
          
    # specific case e.g. need to tell front end that a tile was played by the human or computer 
    def serialize_type(self):
        if self.is_human:
            return "Human"
        else:
            return "Computer"
    
    def serialize_rack(self):
        return self.rack.serialize()  
            