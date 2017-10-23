

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
    
    # specific case e.g. need to tell front end that a tile was played by the human or computer 
    def serialize_type(self):
        if self.is_human:
            return "Human"
        else:
            return "Computer"
            
    def print_player_state(self):
        print("Current running score for " + self.name + ": " + str(self.running_score) + " pts")
        print("Current rack for " + self.name + ": " + ''.join(self.rack))
        print("Words played and scores:")
        for (pos, (word, score)) in enumerate(self.words_played):
            print(str(pos + 1) + ". " + ''.join(word) + " - " + str(score) + " pts")
            