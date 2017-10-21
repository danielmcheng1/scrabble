
#instantiates a player bound to a particular board and common scrabble bag
IS_HUMAN = True
IS_COMPUTER = False
class player:
    def __init__(self, name, is_human, board):
        self.name = name
        self.is_human = is_human
        self.rack = []  
        self.running_score = 0
        self.words_played = []
        
    def print_player_state(self):
        print("Current running score for " + self.name + ": " + str(self.running_score) + " pts")
        print("Current rack for " + self.name + ": " + ''.join(self.rack))
        print("Words played and scores:")
        for (pos, (word, score)) in enumerate(self.words_played):
            print(str(pos + 1) + ". " + ''.join(word) + " - " + str(score) + " pts")
            