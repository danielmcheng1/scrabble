
import rack 

IS_HUMAN = True 
IS_COMPUTER = False 
class Player:
    def __init__(self, is_human):
        self.is_human = is_human
        self.rack = []  
        self.running_score = 0
        self.words_played = []
        
    def is_human(self):
        return self.is_human 
    
    def draw_tiles_at_start_of_game(self, bag):
        self.draw_tiles(bag, rack.MAX_NUM_TILES)
        
    def draw_tiles_at_end_of_turn(self, bag):
        self.draw_tiles(bag, self.rack.MAX_NUM_TILES - self.rack.get_num_tiles())
        
    def draw_tiles(self, bag, n):
        # architecture assumes validation happened in move class 
        num_tiles_to_draw = min(bag.num_tiles_left, n)
        bag.shuffle_bag()
        for i in range(0, num_tiles_to_draw):
            self.rack.add_tile(bag.draw_tile())
            
    def exchange_tiles(self, bag, tiles):
        bag.shuffle_bag() 
        for tile in tiles:
            self.rack.remove_one_tile_with_letter(tile.letter)
            self.rack.add_tile(bag.draw_tile())
            
        
    # specific case e.g. need to tell front end that a tile was played by the human or computer 
    def serialize_type(self):
        if self.is_human:
            return "Human"
        else:
            return "Computer"
            
            